import random
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
                hp = int(modifier.hp * random.uniform(0.8, 1.2))

                # Update stats based on attribute type
                if attr.type == "Thaum":
                    result_stat.thaum_atk += atk
                    result_stat.thaum_def += res
                elif attr.type == "Phys":
                    result_stat.phys_atk += atk
                    result_stat.phys_def += res
                elif attr.type == "Mental":
                    result_stat.men_atk += atk
                    result_stat.men_def += res

                result_stat.hp += hp

    return result_stat


def regex_llm_attribute(generated_attribute):
    # Use regex to find all attributes between square brackets
    pattern = r'\[(.*?)\]'
    matches = re.findall(pattern, generated_attribute)

    # Remove any leading/trailing whitespace from each attribute
    result = [attr.strip() for attr in matches]

    return result


async def process_attributes(desc: str)->Stat:
    Stat()
    atrb_prompt = await prompts.attribute_from_description_prompt(desc)
    print(atrb_prompt)
    generated_attribute = await llmapi.send_to_llm(atrb_prompt)
    print(generated_attribute)
    attributes_list = regex_llm_attribute(generated_attribute.results[0].text)
    print(attributes_list)
    stat = await calculate_stat(attributes_list)
    print(stat)

    return stat
