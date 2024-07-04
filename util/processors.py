import random
from typing import List

from util.models import *
from util import prompts
from util import llmapi
import re
from util import data_manager


async def calculate_stat(input_attributes: list[str]) -> Stat:
    attribute_info = await data_manager.read_attribute_data()
    result_stat = Stat(attributes=input_attributes)

    for attr_name in input_attributes:
        attr = next((a for a in attribute_info.attributes if a.name == attr_name), None)
        if attr:
            modifier = next((m for m in attribute_info.modifier if m.name == attr.stat), None)
            if modifier:
                # Apply 20% random modifier
                atk = int(modifier.atk * random.uniform(0.8, 1.2))
                res = int(modifier.res * random.uniform(0.8, 1.2))
                max_hp = int(modifier.hp * random.uniform(0.8, 1.2))

                # Update stats based on attribute type
                if attr.type == "Thaum":
                    result_stat.thaum_atk += atk
                    result_stat.thaum_res += res
                elif attr.type == "Phys":
                    result_stat.phys_atk += atk
                    result_stat.phys_res += res
                elif attr.type == "Mental":
                    result_stat.men_atk += atk
                    result_stat.men_res += res

                result_stat.hp += hp
                result_stat.max_hp +=hp

    return result_stat


def regex_llm_attribute(generated_attribute):
    # Use regex to find all attributes between square brackets
    pattern = r'\[(.*?)\]'
    matches = re.findall(pattern, generated_attribute)

    return matches  # Directly return the list of matches

#Get Stat from Attribute
async def process_attributes(desc: str, name: str, type: str, level = 5) -> CalculationResult:
    atrb_prompt = await prompts.attribute_from_description_prompt(desc, name, type)
    #print(atrb_prompt)
    generated_attribute = await llmapi.send_to_llm(atrb_prompt)
    #print(generated_attribute)
    attributes_list = regex_llm_attribute(generated_attribute.results[0].text)
    #print(attributes_list)
    stat = await calculate_stat(attributes_list)
    print(stat)
    result = CalculationResult(name, attributes_list[0], stat)
    return result


def regex_llm_choices(text, desc) -> List[Choice]:
    choices = []
    pattern = r'([A-C])\. \[(\w+) Action: (.+?)\]\n\[Material Get: (.+?)\]'
    matches = re.findall(pattern, text)

    for match in matches:
        choice = Choice()
        choice.desc = desc
        choice.type = match[1]  # Physical, Mental, or Thaumaturgic
        choice.action = match[2]  # Add the action description
        choice.materials = [mat.strip().strip('"') for mat in match[3].split(',')]
        choices.append(choice)

    return choices


async def process_choices(desc: str) -> List[Choice]:
    choices_prompt = await prompts.choices_from_description_prompt(desc)
    #print(atrb_prompt)
    generated_choices = await llmapi.send_to_llm(choices_prompt)

    choices_list = regex_llm_choices(generated_choices.results[0].text, desc)

    return choices_list



def regex_llm_materials(text: str) -> list[str]:
    # Use regex to find all text within square brackets
    pattern = r'\[(.*?)\]'
    matches = re.findall(pattern, text)

    # Return the list of matched items
    return matches

async def process_materials(desc: str) -> list[str]:
    material_prompt = await prompts.materials_from_description_prompt(desc)
    # print(atrb_prompt)
    generated_materials = await llmapi.send_to_llm(material_prompt)
    # print(generated_attribute)
    choices_list = regex_llm_materials(generated_materials.results[0].text)

    return choices_list
