import config
from bot.rpg import rpg_prompt
from util import data_manager
from util import discordapi
from util import processors
from util.models import *
#import rpg_prompt


async def generate_new_player():
    while True:
        # Get the Character Creation Request~
        content : CharacterCreationQueueItem= await config.character_creation_queue.get()
        interaction: discord.Interaction = content.interaction
        user: discord.Member = interaction.user
        about = content.description

        # Check if user already have a character
        exist = await check_player_exist(user.display_name)
        player_name = user.display_name
        player_desc = about

        if exist:
            # Tell user that character already exists
            await discordapi.send_webhook_message(interaction.channel, f"The Player {player_name} already exist,user", )
            config.character_creation_queue.task_done()
        else:
            # Make the character
            # Uses default attribute Generator
            player_data = await processors.process_attributes(about, player_name, "Person")
            print(player_data.stat)
            player_data = Player(name=player_name, desc=player_data.desc, stat=player_data.stat)
            player_data.stat.attributes.pop(0)
            # Put new character in za json
            data_manager.write_character_data(player_data)

            # Send the Created Character Result
            generated_player = player_info_string(player_data)
            await discordapi.send_webhook_message(interaction.channel, generated_player)
            config.character_creation_queue.task_done()


def getPlayerInfo(name: str) -> str:
    player_data = data_manager.read_character_data(name)
    if player_data.name != "":
        return player_info_string(player_data)
    else:
        return f"Player {name} don't exist"


def player_info_string(player: Player) -> str:
    #Fancy Piece of Code to Format Character Display
    def format_stat(stat: Stat) -> str:
        stat_lines = []
        if stat.hp > 0:
            stat_lines.append(f"HP: {stat.hp}")
        if stat.phys_atk > 0:
            stat_lines.append(f"Physical Attack: {stat.phys_atk}")
        if stat.phys_def > 0:
            stat_lines.append(f"Physical Defense: {stat.phys_def}")
        if stat.men_atk > 0:
            stat_lines.append(f"Mental Attack: {stat.men_atk}")
        if stat.men_def > 0:
            stat_lines.append(f"Mental Defense: {stat.men_def}")
        if stat.thaum_atk > 0:
            stat_lines.append(f"Thaumaturgical Attack: {stat.thaum_atk}")
        if stat.thaum_def > 0:
            stat_lines.append(f"Thaumaturgical Defense: {stat.thaum_def}")
        if stat.pata_dmg > 0:
            stat_lines.append(f"Pataphysical Damage: {stat.pata_dmg}")
        if stat.pata_rate > 0:
            stat_lines.append(f"Pataphysical Rate: {stat.pata_rate:.2f}")
        if stat.attributes:
            stat_lines.append(f"Attributes: {stat.attributes[0]} and {stat.attributes[1]}")
        return "\n".join(stat_lines)

    def format_equipment(equip: Equipment | None, equip_type: str) -> str:
        if equip.name != "":
            return f"{equip_type}: {equip.name}\n{equip.desc}\n{format_stat(equip.stat)}"
        else:
            return f"No {equip_type.lower()} equipped"

    info = f"""
**{player.name}**
{player.desc}
**Stats:**
{format_stat(player.stat)}
**Equipment:**
{format_equipment(player.weapon, "Weapon")}
{format_equipment(player.armor, "Armor")}
{format_equipment(player.possession, "Possession")}
{format_equipment(player.power, "Power")}
"""
    return info.strip()


async def check_player_exist(name):
    player_list = await data_manager.get_player_list()
    for player in player_list:
        if player == name:
            return True
    return False
