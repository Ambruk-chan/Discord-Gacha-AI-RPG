# Contains General Use Prompts
from util.models import *
from util import data_manager


async def attribute_from_description_prompt(item_desc:str):
    request = GenerationRequest()
    attributes = await data_manager.read_attribute_data()
    attribute_info = format_attribute_info(attributes)
    grammar = create_attributes_grammar(attributes)
    instruction = "Based on the description above, please give 2 fitting attributes for the item/object/person/creature."
    prompt = "USER: "+ attribute_info +"\n" + item_desc + instruction + "\n\n" + "ASSISTANT: "
    request.prompt = prompt
    request.stop_sequence = ["<END>"]
    request.grammar = grammar
    request.grammar_string = grammar
    
    return request

def format_attribute_info(attr_info: AttributeInfo) -> str:
    output = "AttributeInfo:\n"
    
    output += "  Attributes:\n"
    for attr in attr_info.attributes:
        output += f"    - Name: {attr.name}\n"
        output += f"      Description: {attr.desc}\n"
        output += f"      Type: {attr.type}\n"
    
    output += "  Types:\n"
    for type_ in attr_info.types:
        output += f"    - Name: {type_.name}\n"
        output += f"      Description: {type_.desc}\n"
    
    return output

def create_attributes_grammar(attributeinfo: AttributeInfo,max_level:int=1) -> str:
    attribute_list = []
    for attribute in attributeinfo.attributes:
        if attribute.rare <= max_level:
            attribute_list.append(attribute.name)

    grammar_list = format_string_list_for_gbnf(attribute_list)

    grammar =   f"root ::= \"[\"attr\"] [\"attr\"] <END>\" \n \nattr ::= {grammar_list}"
    
    return grammar

def format_string_list_for_gbnf(string_list: list[str]) -> str:
    # Join the strings with "|" and wrap them in quotes
    formatted_items = '\"|\"'.join(string_list)
    
    # Add parentheses and the first and last quotes
    return f'("{formatted_items}")'