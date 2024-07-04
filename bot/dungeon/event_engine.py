import random
import config
from util import data_manager, discordapi
from util.models import *
from util.processors import llmapi


async def dungeon_action():
    while True:
        item: DungeonActionQueueItem = await config.dungeon_action_queue.get()
        interaction = item.interaction
        action = item.action
        player: Player = data_manager.read_character_data(interaction.user.display_name)
        if action_checker(player,interaction):
            dungeon: Dungeon = await data_manager.read_dungeon_data(player.progress.dungeon_name)
            history: DungeonHistory = await data_manager.read_dungeon_history(dungeon)
            if player.progress.position < 6:  # Means player is in the middle of the dungeon
                if isinstance(action,EncounterAction):
                    encounter = dungeon.events[player.progress.position].event
                    if isinstance(encounter, Encounter):
                        # This function writes an entire turn where player chooses something
                        await encounter_handler(player,dungeon,interaction,action,history)
                    else:
                        await discordapi.send_webhook_thread(interaction.channel,"But Nobody Came")
                elif isinstance(action,BattleAction):
                    enemy = dungeon.events[player.progress.position].event
                    if isinstance(enemy,Enemy):
                        attacker = Entity(name = player.name, desc= player.desc, stat=player.stat)
                        target = Entity(name = enemy.name, desc= enemy.desc, stat= enemy.stat)
                        # This function writes an entire turn where player attacks the enemy
                        await battle_handler(attacker,target, dungeon,interaction,action,history)
                    else:
                        await discordapi.send_webhook_thread(interaction.channel,"But Nobody Came")
                elif isinstance(action,PassAction):
                    await pass_handler(player,dungeon,interaction,action,history)
                else:
                    await convo_handler(player,dungeon,interaction,action,history)
        config.dungeon_action_queue.task_done()

# Duck Typing Go BRRRRR
async def battle_handler(attacker: Entity, target: Entity, dungeon,interaction,action,history):
    # This is the Damage Calculation calculated programmatically
    init_meta_battle: str = attacker_battle_action_process(attacker, action)
    init_story_battle: str = action.quip
    if (init_story_battle=="") or (init_story_battle==None):
        quip_prompt = create_battle_quip_prompt(attacker, target, history, init_meta_battle)
        init_story_battle = (await llmapi.send_to_llm(quip_prompt)).results[0].text

    init_record = DungeonRecord(
        type="Battle",
        meta=init_meta_battle,  # Attacker's Battle Action and Calculation and Stat
        story=init_story_battle,  # Attacker's Quip or General Commentary
    )
    # Send attack to discord
    await discordapi.send_webhook_thread(interaction.channel, format_attacker_init(init_record))
    # Save into temp_record
    history.records.append(init_record)

    # Calculate the target's stat and such after they get beaten up
    result_meta_battle: str = attacker_battle_result_process(player, dungeon, action)  # Calculated Result

    # Create the result story or quip
    quip_prompt = create_battle_quip_prompt(history, player, dungeon, result_meta_battle)
    result_story_battle = (await llmapi.send_to_llm(quip_prompt)).results[0].text
    result_record = DungeonRecord(
        type="Battle",
        meta=result_meta_battle,  # Player's Action Result and Enemy Damage and Stat
        story=result_story_battle  # The narration and such
    )
    #  Send the result story to discord
    await discordapi.send_webhook_thread(interaction.channel, format_player_result(init_record))
    # Save into temp_record
    history.records.append(result_record)

    # Save temp_record to Json
    update_history(history)
    return

async def encounter_handler(
    player:Player,
    dungeon:Dungeon,
    interaction:discord.Interaction,
    action:EncounterAction,
    history: DungeonHistory
):
    # This is the Meta Data calculated programmatically
    init_meta_encounter: str = player_choice_process(player, action)
    init_story_encounter: str = action.quip
    if (init_story_encounter == "") or (init_story_encounter == None):
        quip_prompt = create_regular_quip_prompt(history, player, init_meta_encounter)
        init_story_player = (await llmapi.send_to_llm(quip_prompt)).results[0].text
    init_record = DungeonRecord(
        type="Encounter",
        meta=init_meta_encounter,  # Player's Choice (verbatim)
        story=init_story_encounter,  # Player's Quip
    )
    # Send player result to discord
    await discordapi.send_webhook_thread(interaction.channel, format_player_init(init_record))
    # Save into temp_record
    history.records.append(init_record)

    # Calculate if player is successful in their choice (thaum,phys,men check)
    # Also update their stat too
    result_meta_player: str = player_result_process(player, dungeon, action)  # Calculated Result

    # Create the result story
    encounter_prompt = encounter_prompt_creator(history, player, dungeon, result_meta_player)
    result_story_player: str = (await llmapi.send_to_llm(encounter_prompt)).results[0].text
    result_record = DungeonRecord(
        type="Encounter",
        meta=result_meta_player,
        story=result_story_player
    )
    #  Send the result story to discord (Basically the interaction result and material get and stuff)
    await discordapi.send_webhook_thread(interaction.channel, format_player_result(init_record))
    # Save into temp_record
    history.records.append(result_record)

    # Save temp_record to Json
    update_history(history)
    return

async def pass_handler(player, dungeon, interaction, action, history):
    # TODO, work on this
    current_event = dungeon.events[player.progress.position].event
    # Just put up The Meta as doin' nothin'
    init_meta_player: str = f"[{player.name} end their turn]"
    init_story_player: str = action.quip

    if (init_story_player == "") or (init_story_player == None):
        quip_prompt = create_regular_quip_prompt(history, player, init_meta_player)
        init_story_player = (await llmapi.send_to_llm(quip_prompt)).results[0].text

    init_record = DungeonRecord(
        type="Pass",
        meta=init_meta_player,  # Meta Note saying Player just continues
        story=init_story_player,  # Player's Quip
    )
    await discordapi.send_webhook_thread(interaction.channel, format_player_init(init_record))
    history.records.append(init_record)
    if isinstance(current_event, Enemy):
        attacker = Entity(current_event.name,current_event.desc,current_event.stat)
        target = Entity(name = player.name, desc = player.desc,stat=player.stat)
        await battle_handler(attacker, target, dungeon, interaction, action, history)
    elif isinstance(current_event, Encounter):
        await encounter_handler(player, dungeon, interaction, current_event, history)
    update_history(history)
    return

async def convo_handler(player, dungeon, interaction, action, history):
    # Just put in Player just doing handling convo and stuff
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
    history.records.append(init_record)

    # Calculate if player is successful in their choice (thaum,phys,men check)
    # Also update their stat too
    result_meta_convo : str = f"[Interaction Response]"

    # Create the result story
    convo_prompt = encounter_prompt_creator(history, player)
    result_story_convo: str = (await llmapi.send_to_llm(convo_prompt)).results[0].text
    result_record = DungeonRecord(
        type="Conversation",
        meta=result_meta_convo,
        story=result_story_convo
    )
    #  Send the result story to discord (Basically the interaction result and material get and stuff)
    await discordapi.send_webhook_thread(interaction.channel, result_story_convo)
    # Save into temp_record
    history.records.append(result_record)

    # Save temp_record to Json
    update_history(history)
    return

async def action_checker(player,interaction):
    if player.progress.dungeon_name == "":
        # Check if Dungeon Exists
        await discordapi.send_webhook_message(interaction.channel, "You Haven't Created A Dungeon Yet")
        return False
    else:
        dungeon: Dungeon = await data_manager.read_dungeon_data(player.progress.dungeon_name)
        # Check if user is in the dungeon (the thread)
        if dungeon.thread != interaction.channel.id:
            thread_link = f"https://discord.com/channels/{interaction.guild_id}/{dungeon.thread}"
            message = f"this command can only be used in dungeon at {thread_link}"
            await discordapi.send_webhook_message(interaction.channel, message)
            return False
        else:
            return True



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
