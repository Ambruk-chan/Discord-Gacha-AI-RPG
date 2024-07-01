import discord
import config
from util import llmapi
from util import data_manager
from util import processors
from util import discordapi
from util.models import *

async def generate_new_player():
    while True:
        content = await config.process_player_request.get()
        interaction: discord.Interaction = content["interaction_data"]
        user:discord.Member = interaction.user
        about = content["description"]
        print(user.display_name)
        exist = await check_player_exist(user.display_name)
        player_name = user.display_name
        player_desc = about
        if exist:
            await discordapi.send_webhook_message(interaction.channel,f"The Player {player_name} already exist,user",)
            config.process_player_request.task_done()
        else:
            player_stat = await processors.process_attributes(about)
            print(player_stat)
            player_data = Player(name = player_name,desc=player_desc,stat = player_stat)
            
            await data_manager.write_character_data(player_data)

            generated_player = player_info_string(player_data)
            await discordapi.send_webhook_message(interaction.channel,generated_player)
            config.process_player_request.task_done()

def player_info_string(player: Player) -> str:
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
            stat_lines.append(f"Attributes: {', '.join(stat.attributes)}")
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