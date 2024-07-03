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


def format_stat(stat):
    pass


def format_drop(materials):
    pass


def enemy_action_ai(enemy_stat: Stat) -> BattleAction:
    # List of possible actions
    possible_actions = []

    # Check for attack actions
    if enemy_stat.phys_atk > 0:
        possible_actions.append((ActionType.ATTACK, DamageType.PHYSICAL))
    if enemy_stat.men_atk > 0:
        possible_actions.append((ActionType.ATTACK, DamageType.MENTAL))
    if enemy_stat.thaum_atk > 0:
        possible_actions.append((ActionType.ATTACK, DamageType.THAUMATURGIC))

    # Check for defend actions
    if enemy_stat.phys_res > 0:
        possible_actions.append((ActionType.DEFEND, DamageType.PHYSICAL))
    if enemy_stat.men_res > 0:
        possible_actions.append((ActionType.DEFEND, DamageType.MENTAL))
    if enemy_stat.thaum_res > 0:
        possible_actions.append((ActionType.DEFEND, DamageType.THAUMATURGIC))

    # Always include FLEE as an option
    possible_actions.append((ActionType.FLEE, None))

    # Choose a random action
    chosen_action, chosen_type = random.choice(possible_actions)

    # Generate a random quip

    return BattleAction(action=chosen_action, type=chosen_type, quip="")

def calculate_battle(attacker:Stat, target:Stat, action:BattleAction):
    if action.action == ActionType.ATTACK:
        damage = 0
        if action.type == DamageType.PHYSICAL:
            damage = max(0, attacker.phys_atk - target.phys_res)
            target.hp -= damage
            target.thaum_res = max(0, target.thaum_res - damage // 2)
        elif action.type == DamageType.MENTAL:
            damage = max(0, attacker.men_atk - target.men_res)
            target.hp -= damage
            target.phys_res = max(0, target.phys_res - damage // 2)
        elif action.type == DamageType.THAUMATURGIC:
            damage = max(0, attacker.thaum_atk - target.thaum_res)
            target.hp -= damage
            target.men_res = max(0, target.men_res - damage // 2)

    elif action.action == ActionType.DEFEND:
        if action.type == DamageType.PHYSICAL:
            target.men_res += attacker.phys_def // 2
        elif action.type == DamageType.MENTAL:
            target.thaum_res += attacker.men_def // 2
        elif action.type == DamageType.THAUMATURGIC:
            target.phys_res += attacker.thaum_def // 2

    # For FLEE action, we don't modify any stats

    return BattleResult(attacker=attacker, target=target)

async def player_action(action) -> DungeonAction:
    enemy: Enemy = action.dungeon.events[action.floor].event
    if action.player.turn == False:
        action.result = f"{action.player.name} tried to act, but it's not their turn yet~"
        return action
    else:
        # Player chooses an action (ATK or DEF)
        player_action: BattleAction = action.battle_action  # Assuming this is set elsewhere

        # Calculate Damage ETC
        battle_result: BattleResult = calculate_battle(attacker=action.player.stat, target=enemy.stat, action=player_action)

        # Create the Narration
        player_action_prompt = dungeon_prompt.player_action_prompt(action, battle_result)
        player_action.quip = (await llmapi.send_to_llm(player_action_prompt)).results[0].text

        # Save All That In The Action Data Class
        action.player.stat = battle_result.attacker
        enemy.stat = battle_result.target
        player_stat = format_stat(action.player.stat)

        if enemy.stat.hp > 0:
            action.result = f"{player_action.quip}\n{player_stat}"
            action.player.turn = False
            enemy.turn += 1
        else:
            # Enemy is dead, do this
            # Create Enemy Death Scene
            enemy_defeat_prompt = dungeon_prompt.enemy_defeat_prompt(action)
            player_action.quip = (await llmapi.send_to_llm(enemy_defeat_prompt)).results[0].text
            # Create Enemy Drop
            enemy_drop = format_drop(enemy.materials)
            action.player.materials.append(enemy.materials)
            action.result = f"{player_action.quip}\n{enemy_drop}"
            action.player.turn = False
            action.player.floor += 1

    return action

async def enemy_action(action)->DungeonAction:
    enemy:Enemy = action.dungeon.events[action.floor].event
    if (enemy.turn == 0):
        # Enemy Does Introduce Itself
        enemy_intro_prompt = dungeon_prompt.enemy_intro_prompt(action)
        enemy_intro = (await llmapi.send_to_llm(enemy_intro_prompt)).results[0].text
        enemy_stat = format_stat(enemy.stat)
        action.result = f"{enemy_intro}\n{enemy_stat}"
        action.player.turn = True
    else:
        # Enemy Does Something (in the system)
        # Either ATK or DEF
        enemy_action:BattleAction = enemy_action_ai(enemy.stat)
        # Calculate Damage ETC
        battle_result:BattleResult = calculate_battle(attacker = enemy.stat, target = action.player.stat, action = enemy_action)
        # Create the Narration
        enemy_action_prompt = dungeon_prompt.enemy_action_prompt(action,battle_result)
        enemy_action.quip = (await llmapi.send_to_llm(enemy_action_prompt)).results[0].text
        # Save All That In The Action Data Class
        action.player.stat = battle_result.target
        enemy.stat = battle_result.attacker
        enemy_stat = format_stat(enemy.stat)
        if action.player.stat.hp >0:
            action.result = f"{enemy_action.quip}\n{enemy_stat}"
            action.player.turn = True
        else:
            # Player is dead, just kick them out of the dungeon
            action.player.turn = False
            action.player.progress.position = -1
            action.player.progress.dungeon_name =""
            action.result = f"{enemy_action.quip}\n{enemy_stat}"
    return action

async def battle_event(action:DungeonAction) -> DungeonAction:
    if action.action is None:
        return await enemy_action(action)
    elif action.player.turn:
        return await player_action(action)
    else:
        return await enemy_action(action)

def encounter_event(action:DungeonAction):
    pass


async def event_trigger(dungeon, player, interaction:discord.Interaction, decision)->DungeonAction:
    history = await discordapi.get_thread_history(interaction.channel)
    if decision is None:
        player.progress.position = 0
    floor = player.progress.position
    event = dungeon.events[floor].event
    action = DungeonAction(dungeon,history, player, floor,decision)
    if isinstance(event, Enemy):
        return await battle_event(action)
    elif isinstance(event, Encounter):
        return await encounter_event(action)
    else:
        return action


async def dungeon_action():
    while True:
        item : DungeonAdvanceQueueItem = await config.dungeon_advance_queue.get()
        interaction = item.interaction
        action = item.action
        player: Player = data_manager.read_character_data(interaction.user.display_name)
        if player.progress.position ==-1: # Means player haven't started the dungeon yet
            await start_dungeon(interaction,player)
        elif player.progress.position <6: # Means player is in the middle of the dungeon
            await advance_dungeon(interaction,player,action)
        else:
            await exit_dungeon(interaction,player)
async def start_dungeon(interaction,player):
    if player.progress.dungeon_name == "":
        await discordapi.send_webhook_message(interaction.channel, "You Haven't Created A Dungeon Yet")
        config.dungeon_advance_queue.task_done()
    else:
        dungeon: Dungeon = await data_manager.read_dungeon_data(player.progress.dungeon_name)
        if dungeon.thread != interaction.channel:
            thread_link = f"https://discord.com/channels/{interaction.guild_id}/{dungeon.thread}"
            message = f"this command can only be used in dungeon at {thread_link}"
            await discordapi.send_webhook_message(interaction.channel, message)
            config.dungeon_advance_queue.task_done()
        else:
            response : DungeonAction = await event_trigger(dungeon, player, interaction,None)
            await data_manager.write_character_data(response.player)
            await data_manager.write_dungeon_data(response.dungeon)
            await discordapi.send_webhook_message(interaction.channel, response.result)
            config.dungeon_advance_queue.task_done()

async def advance_dungeon(interaction, player, action):
    dungeon: Dungeon = await data_manager.read_dungeon_data(player.progress.dungeon_name)
    if dungeon.thread != interaction.channel:
        thread_link = f"https://discord.com/channels/{interaction.guild_id}/{dungeon.thread}"
        message = f"This command can only be used in the dungeon at {thread_link}"
        await discordapi.send_webhook_message(interaction.channel, message)
        config.dungeon_advance_queue.task_done()
    else:
        response: DungeonAction = await event_trigger(dungeon, player, interaction, action)
        await data_manager.write_character_data(response.player)
        await data_manager.write_dungeon_data(response.dungeon)
        await discordapi.send_webhook_message(interaction.channel, response.result)

        if response.player.progress.position >= 6:  # Check if player has reached the end of the dungeon
            epilogue = await exit_dungeon(interaction, response.player)
            await discordapi.send_webhook_message(interaction.channel,epilogue)
        config.dungeon_advance_queue.task_done()

async def exit_dungeon(interaction,player)->str:
    dungeon: Dungeon = await data_manager.read_dungeon_data(player.progress.dungeon_name)
    history = await discordapi.get_thread_history(interaction.channel)
    epilogue_prompt = dungeon_prompt.epilogue_prompt(dungeon,history)
    epilogue_response = await llmapi.send_to_llm(epilogue_prompt)
    epilogue = epilogue_response.results[0].text
    return epilogue

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
            # Write the dungeon data to JSON
            await data_manager.write_dungeon_data(created_dungeon)

            # Create a link to the thread
            thread_link = f"https://discord.com/channels/{content.interaction.guild_id}/{thread.id}"

            # Send a message with the thread link
            message = f"Dungeon Created at {thread_link}"
            await util.discordapi.send_webhook_message(content.interaction.channel, message)
        else:
            error = "You already created a dungeon, use /dungeon abandon to destroy it"
            await util.discordapi.send_webhook_message(content.interaction.channel, error)
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
