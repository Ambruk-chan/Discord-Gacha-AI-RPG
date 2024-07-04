import random

import discord

import config
from bot.dungeon import event_util, event_prompt
from util import data_manager, discordapi
from util.models import *
from util.processors import llmapi


async def dungeon_action():
    while True:
        item: DungeonActionQueueItem = await config.dungeon_action_queue.get()
        interaction = item.interaction
        action = item.action
        exploration = action_checker(interaction)
        thread = interaction.channel
        if exploration:
            player = exploration.player
            if exploration.floor < 6:  # Means player is in the middle of the dungeon
                if isinstance(action, EncounterAction):
                    encounter = exploration.dungeon.events[exploration.floor].event
                    if isinstance(encounter, Encounter):
                        # This function writes an entire turn where player chooses something
                        await encounter_handler(exploration, action, interaction)
                    else:
                        # If the player for some reason chooses 'choice' in the middle of  a battle
                        await discordapi.send_webhook_thread(thread, "But Nobody Came")
                elif isinstance(action, BattleAction):
                    next_event = exploration.dungeon.events[exploration.floor].event
                    if exploration.enemy:
                        attacker = exploration.player
                        target = exploration.enemy
                        # This function writes an entire turn where player attacks the enemy
                        await battle_handler(attacker, target, exploration, action, interaction)
                    else:
                        #There's no enemy tho...
                        await discordapi.send_webhook_thread(interaction.channel, "But Nobody Came")
                elif isinstance(action, PassAction):
                    await pass_handler(exploration, action, interaction)
                else:
                    await convo_handler(exploration, action, interaction)
        config.dungeon_action_queue.task_done()


# Fixed Duck Typing
async def battle_handler(attacker: Entity, target: Entity, exploration: DungeonHistory, action, interaction, ):
    # This is the Damage Calculation calculated programmatically
    #init_meta_battle: str = event_util.attacker_battle_init_process(attacker, action)
    init_meta_battle = f"{attacker.name} uses {action.type.name} move!"
    init_story_battle: str = action.quip
    # Duck typing with exploration, it basically want a log, will fix it later
    if (init_story_battle == "") or (init_story_battle == None):
        quip_prompt = event_prompt.create_battle_quip_prompt(attacker, target, exploration, init_meta_battle)
        init_story_battle = (await llmapi.send_to_llm(quip_prompt)).results[0].text

    init_record = DungeonRecord(
        type="Battle",
        meta=init_meta_battle,  # Attacker's Battle Action and Calculation and Stat
        story=init_story_battle,  # Attacker's Quip or General Commentary
    )
    # Send attack to discord
    await discordapi.send_webhook_thread(interaction.channel, event_util.format_record(init_record))
    # Save into temp_record
    exploration.records.append(init_record)
    battle_result: BattleResult = event_util.attacker_battle_result_process(attacker, target,
                                                                            exploration)  # Calculated Result
    # Calculate the target's stat and such after they get beaten up
    result_meta_battle = battle_result.meta_info  # Calculated Result

    # Create the result story or quip
    quip_prompt = event_prompt.create_battle_quip_prompt(attacker, target, exploration, result_meta_battle)
    result_story_battle = (await llmapi.send_to_llm(quip_prompt)).results[0].text
    result_record = DungeonRecord(
        type="Battle",
        meta=result_meta_battle,  # Player's Action Result and Enemy Damage and Stat
        story=result_story_battle  # The narration and such
    )
    #  Send the result story to discord
    await discordapi.send_webhook_thread(interaction.channel, event_util.format_record(init_record))
    # Save into temp_record
    exploration.records.append(result_record)

    # Save temp_record to Json
    data_manager.write_exploration_data(exploration)
    return


async def encounter_handler(
    exploration: DungeonHistory,
    action: EncounterAction,
    interaction: discord.Interaction
):
    player = exploration.player
    encounter = exploration.dungeon.events[exploration.floor].event
    if action.choice == "A":
        encounter_choice = encounter.choices[0].desc
    elif action.choice == "B":
        encounter_choice = encounter.choices[1].desc
    elif action.choice == "C":
        encounter_choice = encounter.choices[2].desc
    else:
        return
    # This is the Metadata containing player's choice
    init_meta_encounter: str = f"{player.name} has (finally) decided to {encounter_choice}"
    init_story_encounter: str = action.quip
    if (init_story_encounter == "") or (init_story_encounter == None):
        quip_prompt = event_prompt.create_regular_quip_prompt(exploration, player, init_meta_encounter)
        init_story_encounter = (await llmapi.send_to_llm(quip_prompt)).results[0].text

    init_record = DungeonRecord(
        type="Encounter",
        meta=init_meta_encounter,  # Player's Choice (verbatim)
        story=init_story_encounter,  # Player's Quip
    )
    exploration.records.append(init_record)
    # Send player result to discord
    await discordapi.send_webhook_thread(interaction.channel, event_util.format_record(init_record))
    # Save into temp_record
    # Calculate if player is successful in their (thaum,phys,men) check
    # Then put it in encounter_result the narration and such
    encounter_result: ActionResult = event_util.encounter_result_process(exploration, action)

    # Check for any change in material

    if encounter_result.material_change is not None:
        exploration.materials = encounter_result.material_change
    # Check for any change in stat

    if encounter_result.stat_change is not None:
        exploration.player.stat = encounter_result.stat_change

    result_meta_encounter = encounter_result.meta_info
    # Create the result story
    encounter_prompt = event_prompt.create_regular_quip_prompt(exploration, result_meta_encounter)
    result_story_encounter: str = (await llmapi.send_to_llm(encounter_prompt)).results[0].text

    result_record = DungeonRecord(
        type="Encounter",
        meta=result_meta_encounter,
        story=result_story_encounter
    )
    #  Send the result story to discord (Basically the interaction result and material get and stuff)
    await discordapi.send_webhook_thread(interaction.channel, event_util.format_record(result_record))
    # Save into temp_record

    exploration.records.append(result_record)

    # Save temp_record to Json
    data_manager.write_exploration_data(exploration)
    return


async def next_event_handler(exploration, interaction):
    exploration.floor += 1
    new_event = exploration.dungeon.events[exploration.floor].event

    if isinstance(new_event, Enemy):
        init_meta_new_event: str = f"{new_event.name} is making an appearance!"
        entry_prompt = event_prompt.create_regular_quip_prompt(exploration, new_event, init_meta_new_event)
        init_story_new_event = (await llmapi.send_to_llm(entry_prompt)).results[0].text
        exploration.enemy = new_event
        init_record = DungeonRecord(
            type="Enemy",
            meta=init_meta_new_event,  # Player's Choice (verbatim)
            story=init_story_new_event,  # Player's Quip
        )
    else:
        init_meta_new_event: str = f"{exploration.player.name} has encountered {new_event.name}!"
        entry_prompt = event_prompt.create_regular_quip_prompt(exploration, new_event, init_meta_new_event)
        init_story_new_event = (await llmapi.send_to_llm(entry_prompt)).results[0].text

        init_record = DungeonRecord(
            type="Encounter",
            meta=init_meta_new_event,  # Player's Choice (verbatim)
            story=init_story_new_event,  # Player's Quip
        )
    exploration.records.append(init_record)
    # Send player result to discord
    await discordapi.send_webhook_thread(interaction.channel, event_util.format_record(init_record))
    # Save into temp_record
    data_manager.write_exploration_data(exploration)
    return


async def game_over_handler(exploration, interaction):
    pass


async def pass_handler(exploration, action: PassAction, interaction: discord.Interaction):
    # This is the 'End Turn' function. It will also advance the floor if all obstacle has been cleared.
    current_event = exploration.dungeon.events[exploration.floor].event
    player = exploration.player
    # Just put up The Meta as doin' nothin'
    init_meta_player: str = f"[{player.name} end their turn]"
    init_story_player: str = action.quip

    if (init_story_player == "") or (init_story_player == None):
        quip_prompt = event_prompt.create_regular_quip_prompt(exploration, player)
        init_story_player = (await llmapi.send_to_llm(quip_prompt)).results[0].text

    init_record = DungeonRecord(
        type="Pass",
        meta=init_meta_player,  # Meta Note saying Player just ended their turn
        story=init_story_player,  # Player's Quip, will be generated if none
    )

    await discordapi.send_webhook_thread(interaction.channel, event_util.format_record(init_record))
    exploration.records.append(init_record)

    # Now decide what to do after player ended their turn
    if isinstance(current_event, Enemy):
        if exploration.enemy.stat.hp > 0:  # Enemy is still alive, it's enemy's turn
            attacker = exploration.enemy
            target = exploration.player
            ai_action = enemy_action_ai(attacker.stat)
            await battle_handler(attacker, target, exploration, ai_action, interaction)
        elif exploration.player.stat.hp < 1:  # You're Dead!
            await game_over_handler(exploration, interaction)
        else:  # Enemy is dead, let's move on
            exploration.enemy = None  # Mark enemy is dead
            exploration.materials += current_event.materials  # Get Ze Drops
            await next_event_handler(exploration, interaction)
    else:  # Move on / flee from an encounter
        await next_event_handler(exploration, interaction)
    return


async def convo_handler(exploration, action, interaction):
    # Just put in Player just doing handling convo and stuff
    player = exploration.player
    init_meta_convo: str = f"[{player.name} decides to interact]"
    init_story_convo: str = action.quip
    if (init_story_convo == "") or (init_story_convo == None):
        return
    init_record = DungeonRecord(
        type="Conversation",
        meta=init_meta_convo,  # Player's Choice (verbatim)
        story=init_story_convo,  # Player's Quip
    )
    # Send player result to discord
    await discordapi.send_webhook_thread(interaction.channel, init_story_convo)
    # Save into temp_record
    exploration.records.append(init_record)

    # Calculate if player is successful in their choice (thaum,phys,men check)
    # Also update their stat too
    result_meta_convo: str = f"[Interaction Response]"

    # Create the result story
    convo_prompt = event_prompt.create_regular_quip_prompt(exploration, player, result_meta_convo)
    result_story_convo: str = (await llmapi.send_to_llm(convo_prompt)).results[0].text
    result_record = DungeonRecord(
        type="Conversation",
        meta=result_meta_convo,
        story=result_story_convo
    )
    #  Send the result story to discord (Basically the interaction result and material get and stuff)
    await discordapi.send_webhook_thread(interaction.channel, result_story_convo)
    # Save into temp_record
    exploration.records.append(result_record)

    # Save temp_record to Json
    data_manager.write_exploration_data(exploration)
    return


def action_checker(interaction) -> DungeonHistory | None:
    id = interaction.channel.id
    if isinstance(interaction.channel, discord.Thread):
        exploration: DungeonHistory = data_manager.read_exploration_data(id)
        if interaction.user.display_name == exploration.user:
            return exploration

    return None


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


def calculate_battle(attacker: Stat, target: Stat, action: BattleAction):
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
