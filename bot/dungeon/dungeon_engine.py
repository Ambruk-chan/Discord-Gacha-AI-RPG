import random
import re
from typing import List

import discord

import config
import util.discordapi
from bot.dungeon import dungeon_prompt
from util import data_manager, processors, discordapi
from util.models import *
from util.processors import llmapi

async def enter_dungeon():
    while True:
        content: DungeonEnterQueueItem = await config.dungeon_enter_queue.get()
        dungeon = await data_manager.read_dungeon_data(content.dungeon_name)
        if isinstance(content.player,Player):
            player = Entity(name=content.player.name,desc = content.player.desc, stat = content.player.stat)
        elif isinstance(content.player,Summon):
            player = Entity(name=content.player.name, desc=content.player.desc, stat=content.player.stat)
        else:
            return
        exploration  = DungeonHistory(
            thread_id = content.interaction.channel,
            user=content.interaction.user.display_name,
            player =player,
            enemy = None,
            records = None,
            dungeon = dungeon,
            floor = 0,
            materials= None
        )
        dungeon_start_prompt = dungeon_prompt.dungeon_starting_prompt(player,dungeon)
        meta_start_message = f"[This marks the beginning of {player.name}'s Journey within {dungeon.name}"
        welcome_message = (await llmapi.send_to_llm(dungeon_start_prompt)).results[0].text
        message = await content.interaction.channel.send("Starting Dungeon~")
        thread = await content.interaction.channel.create_thread(name=dungeon.name, message=message)
        await discordapi.send_webhook_thread(thread,f"{welcome_message}")
        starting_record = list[DungeonRecord(
            type = "Encounter",
            meta = meta_start_message,
            story = welcome_message
        )]
        exploration.records = starting_record
        data_manager.write_exploration_data(exploration)
        await config.dungeon_action_queue.task_done()

async def create_dungeon():
    while True:
        content: DungeonCreationQueueItem = await config.dungeon_creation_queue.get()
        material = content.material
        dungeon_information_prompt = dungeon_prompt.dungeon_creation_prompt(material)
        generated_dungeon = await llmapi.send_to_llm(dungeon_information_prompt)
        dungeon_information = generated_dungeon.results[0].text
        dungeon_structure = parse_dungeon_events(dungeon_information)

        # Finalize the Dungeon with interactions and enemy stats
        created_dungeon: Dungeon = await enrich_dungeon(dungeon_structure)

        # Write the dungeon data to JSON
        await data_manager.write_dungeon_data(created_dungeon)

        # Send a message with the thread link
        message = f"Dungeon Created! Name: {created_dungeon.name}"
        await discordapi.send_webhook_message(content.interaction.channel, message)
        config.dungeon_creation_queue.task_done()


async def enrich_dungeon(dungeon: Dungeon) -> Dungeon:
    enriched_events = []

    for event in dungeon.events:
        if isinstance(event.event, Encounter):
            # Enrich Encounter
            choices = await generate_choices(event.event.description)
            enriched_encounter: Encounter = event.event
            enriched_encounter.choices = choices
            enriched_events.append(enriched_encounter)

        elif isinstance(event.event, Enemy):
            # Enrich Enemy
            materials = await generate_materials(event.event.desc)
            stat: Stat = await generate_stat(event.event.desc, event.event.name, "Creature")

            enriched_enemy: Enemy = event.event
            enriched_enemy.stat = stat
            enriched_enemy.materials = materials
            enriched_events.append(enriched_enemy)
    dungeon.event = enriched_events
    return dungeon


def parse_dungeon_events(text):
    # Extract dungeon name
    dungeon_name = re.search(r'\[Dungeon: (.+?)\]', text).group(1)

    # Parse events
    event_matches = re.findall(r'\[Event \d+: (\w+)(?: Battle)?\s*(?:Enemy: (.+?))?\s*Description: (.+?)\]', text,
                               re.DOTALL)

    events = []

    for event_type, enemy_name, description in event_matches:
        if event_type == "Encounter":
            events.append(Event(event=Encounter(description=description.strip())))
        elif event_type in ["Battle", "Boss"]:
            events.append(Event(event=Enemy(name=enemy_name.strip(), desc=description.strip())))

    return Dungeon(name=dungeon_name, events=events)


async def generate_choices(desc):
    result: List[Choice] = await processors.process_choices(desc)
    return result


async def generate_stat(desc, name, type) -> Stat:
    result: CalculationResult = await processors.process_attributes(desc, name, type)
    result.stat.attributes.pop(0)
    return result.stat


async def generate_materials(desc):
    result: list[str] = await processors.process_materials(desc)
    return result
