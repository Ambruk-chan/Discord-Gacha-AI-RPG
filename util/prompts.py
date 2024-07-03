# Contains General Use Prompts
from util.models import *
from util import data_manager


async def attribute_from_description_prompt(item_desc: str, name: str = "Not Decided", type: str = "Object", level=5):
    request = GenerationRequest()
    attributes = await data_manager.read_attribute_data()
    attribute_info = format_attribute_info(attributes)
    grammar = create_attributes_grammar(name, type, attributes, level)
    prompt = f"Analyze the given input based on the following data:{attribute_info}\n\n\nBased on the description given by User, Attribute Creator will give 2 fitting attributes for the item.\n\n### Instruction:\nUser: A fish\n\n### Response:\nAttribute Creator: Fish's Summary: [a regular water-bound creature. Being a simple creature that they are, fishes are attuned naturally to the element of water.]\n\nAttributes: [Natural],[Elemental]<END>\n\n### Instruction:\nUser: {item_desc}\n\n### Response (1 paragraphs, descriptive, creative):\nAttribute Creator:"
    request.prompt = prompt
    request.stop_sequence = ["<END>"]
    request.grammar = grammar
    request.grammar_string = grammar
    request.max_length = 512
    request.max_tokens = 512

    return request


async def choices_from_description_prompt(desc, player):
    request = GenerationRequest()
    grammar = create_choices_grammar()
    prompt = f"{player.desc}\n\nBelow is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\nUser will give Choice Creator a situation, Choice Creator will then make 3 possible options that {player.name} can make.\n\nThere are 3 types of action: Physical, Mental, and Thaumaturgic.\n### Instruction:\nUser: An old mining entrance hidden behind overgrown foliage leads you down a winding path, lit only by the flickering torches set into the rock wall. The air smells of damp earth and dust as you descend deeper into the mountain.\n\n### Response:\nChoice Creator: A. [Physical Action: Use a pickaxe to chip away at a suspicious-looking section of the rock wall]\n[Material Get: \"Ore Sample\", \"Gemstone\"]\nB. [Mental Action: Focus your senses to detect any unusual sounds or vibrations in the tunnel]\n[Material Get: \"Echo Map\", \"Seismic Data\"]\nC. [Thaumaturgic Action: Cast a divination spell to reveal hidden treasures within the nearby rock]\n[Material Get: \"Magical Residue\", \"Ancient Artifact\"]\n\n### Instruction:\nUser: A room filled with forgotten machinery hums quietly as levers and gears turn on their own. It seems to have been abandoned in haste, left to rust in the dim light.\n\n### Response:\nChoice Creator: A. [Physical Action: Attempt to operate one of the still-functioning machines by pulling levers and turning gears]\n[Material Get: \"Mechanical Part\", \"Strange Blueprint\"]\nB. [Mental Action: Analyze the layout and function of the machinery, trying to decipher its purpose]\n[Material Get: \"Technical Insight\", \"Memory Fragment\"]\nC. [Thaumaturgic Action: Channel spiritual energy to commune with the residual echoes of the machine's past operators]\n[Material Get: \"Ethereal Oil\", \"Phantom Tool\"]\n\n### Instruction:\nParadox: {desc}\n\n### Response(1 paragraphs, descriptive, creative):\nChoice Creator:"
    request.prompt = prompt
    request.stop_sequence = ["<END>"]
    request.grammar = grammar
    request.grammar_string = grammar
    request.max_length = 512
    request.max_tokens = 512

    return request


async def materials_from_description_prompt(desc):
    request = GenerationRequest()
    grammar = create_materials_grammar()
    prompt = f"Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\nParadox will give Material Generator a situation or a battle or an enemy description.\n\nMaterial Generator will then write down a list of items that they can get from winning that encounter.\n### Instruction:\nParadox: A sturdy dwarf-like creature made entirely of obsidian, with a broad axe and an iron will. His dark eyes blaze with determination, reflecting the torchlight. He stands guard over a hoard of valuable mithril ore.\n\n### Response:\nMaterial Generator: [Obsidian Shard],[Mithril Ore],[Dwarven Torch]\n\n### Instruction:\nParadox: A curvaceous beauty with supple, tanned skin and flowing hair the color of rich topsoil. Her breasts and hips swell enticingly, barely contained by leaves woven into a intricate harness. Gaia's eyes smolder with a primal allure, and her touch can coax even the most reluctant plants to bloom. She sings in a husky voice, causing the very earth to tremble with desire as roots burst forth from the ground, ensnaring her foes.\n\n### Response:\nMaterial Generator: [Wild Flower Necklace],[Vine Whip],[Tropical Leaf]\n\n### Instruction:\nParadox: {desc}.\n\n### Response:\nMaterial Generator:"
    request.prompt = prompt
    request.stop_sequence = ["<END>"]
    request.grammar = grammar
    request.grammar_string = grammar
    request.max_length = 512
    request.max_tokens = 512

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


def create_attributes_grammar(item_name, item_type, attribute_info: AttributeInfo, max_level: int = 5) -> str:
    attribute_list = []
    for attribute in attribute_info.attributes:
        if attribute.rare <= max_level:
            attribute_list.append(attribute.name)

    grammar_attribute_list = format_string_list_for_gbnf(attribute_list)

    grammar = f"root ::= \"{item_type} Summary: [{item_name} is \"[^\r\n\x0b\x0c\x85\u2028\u2029]+\"]\n\n{item_name}'s Main Attribute: [\"attr\"] [\"attr\"] <END>\" \n\nattr ::= {grammar_attribute_list}"

    return grammar



def create_choices_grammar() -> str:
    grammar = f"root ::= \"A. [Physical \" desc \"\\n\" mat \"\\nB. [Mental \" desc \"\\n\" mat \"\\nC. [Thaumaturgic \" desc \"\\n\" mat \"<END>\"\n\nencounter ::= desc mat\n\ndesc ::= \"Action: \" paragraph \"]\"\nmat ::= \"[Material Get: \\\"\" word \"\\\",\\\"\"word\"\\\"]\"\n\nnum ::= (\"1\"|\"2\"|\"3\"|\"4\"|\"5\"|\"6\"|\"7\"|\"8\"|\"9\")\n\nparagraph ::= [^\\r\\n\\x0b\\x0c\\x85\\u2028\\u2029\\]]+\n\nword ::= [^\\r\\n\\x0b\\x0c\\x85\\u2028\\u2029\\]\\\"]+"

    return grammar


def create_materials_grammar():
    grammar = f"root ::= \"[\"word\"],[\"word\"],[\"word\"]\"\n\nparagraph ::= [^\\r\\n\\x0b\\x0c\\x85\\u2028\\u2029\\]]+\n\nword ::= [^\\r\\n\\x0b\\x0c\\x85\\u2028\\u2029\\]\\\"]+"

    return grammar


def format_string_list_for_gbnf(string_list: list[str]) -> str:
    # Join the strings with "|" and wrap them in quotes
    formatted_items = '\"|\"'.join(string_list)

    # Add parentheses and the first and last quotes
    return f'("{formatted_items}")'
