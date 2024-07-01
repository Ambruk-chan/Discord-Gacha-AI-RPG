from ...util.models import *
import discord
from .rpg_prompt import *
import config
from ...util import llmapi
from ...util import data_manager


async def generate_new_player(user:discord.Member, about:str):
    config.process_player_request.put_nowait(True)
    player_name = user.display_name
    player_desc = about
    player_stat = await process_attributes(about)
    player_data = Player(name = player_name,desc=player_desc,stat = player_stat)
    
    data_manager.write_character_data(player_data)

    generated_player:str = ""

    
    return 


def calculate_stat(attributes):
    stat = Stat()
    stat.attributes = attributes
    

    return stat

def regex_llm_attribute(generated_attribute):


    return 

async def process_attributes(desc:str):
    stat:Stat = Stat()
    atrb_prompt = attribute_from_description_prompt(desc)
    generated_attribute = llmapi.send_to_llm(atrb_prompt)
    attributes_list = regex_llm_attribute(generated_attribute)
    stat = calculate_stat(attributes_list)
    return stat
    


