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

async def create_dungeon():
    while True:
        content: DungeonCreationQueueItem = await config.dungeon_creation_queue.get()
        name = content.interaction.user.display_name
        material = content.material
        player_data = data_manager.read_character_data(name)
        if player_data.progress.dungeon_name == "":
            dungeon_information_prompt = dungeon_prompt.dungeon_creation_prompt(material, player_data)
            generated_dungeon = await llmapi.send_to_llm(dungeon_information_prompt)
            dungeon_information = generated_dungeon.results[0].text
            dungeon_structure = parse_dungeon_events(dungeon_information)

            created_dungeon: Dungeon = await enrich_dungeon(dungeon_structure, player_data)
            # Create a new thread in the current channel
            thread = await content.interaction.channel.create_thread(
                name=f"Dungeon: {created_dungeon.name}",
                auto_archive_duration=1440  # Set to 24 hours, adjust as needed
            )
            created_dungeon.thread = thread.id
            first = created_dungeon.events[0].event.description

            # Write the dungeon data to JSON
            await data_manager.write_dungeon_data(created_dungeon)

            # Send a warm Dungeon Welcome in Thread
            await discordapi.send_webhook_thread(thread,first)

            # Create a link to the thread
            thread_link = f"https://discord.com/channels/{content.interaction.guild_id}/{thread.id}"

            # Send a message with the thread link
            message = f"Dungeon Created at {thread_link}"
            await discordapi.send_webhook_message(content.interaction.channel, message)
        else:
            error = "You already created a dungeon, use /dungeon abandon to destroy it"
            await discordapi.send_webhook_message(content.interaction.channel, error)
        config.dungeon_creation_queue.task_done()


async def enrich_dungeon(dungeon: Dungeon, player: Player) -> Dungeon:
    enriched_events = []

    for event in dungeon.events:
        if isinstance(event.event, Encounter):
            # Enrich Encounter
            choices = await generate_choices(event.event.description, player)
            enriched_encounter: Encounter = event.event
            enriched_encounter.choices = choices
            enriched_events.append(enriched_encounter)

        elif isinstance(event.event, Enemy):
            # Enrich Enemy
            materials = await generate_materials(event.event.desc)
            stat: Stat = await generate_stat(event.event.desc, event.event.name)

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


async def generate_choices(desc, player):
    result: List[Choice] = await processors.process_choices(desc, player)
    return result


async def generate_stat(desc, name) -> Stat:
    result: CalculationResult = await processors.process_attributes(desc, name, "Creature")
    result.stat.attributes.pop(0)
    return result.stat


async def generate_materials(desc):
    result: list[str] = await processors.process_materials(desc)
    return result
