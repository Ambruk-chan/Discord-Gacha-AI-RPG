import asyncio
import re

import apiconfig
import config
from util import llmapi
from util.data_manager import read_attribute_data, write_attribute_data
from util.models import *


async def getAttributeDescPrompt(word):
    request = GenerationRequest()
    grammar = ""
    prompt = f"Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\nGiven a word given by Paradox, Descriptor will generate a short one paragraph description of how the word describes a person and  an object in relation to RPG.\n### Instruction:\nParadox: Newtonian\n\n### Response:\nDescriptor: Entities or objects imbued with \"Newtonian\" qualities embody the rigid, clockwork precision of classical physics. They exude an aura of mathematical certainty, their movements and actions governed by immutable laws of motion and force. Newtonian creations radiate an air of mechanical reliability, their existence a testament to the predictable, measurable nature of the physical world in all its mathematical glory.\n\n### Instruction:\nParadox: Elemental\n\n### Response:\nDescriptor: Entities or artifacts bearing the \"Elemental\" quality pulsate with the raw, primordial essence of the five elements. Fire, Water, Air, Earth, and Lightning. They embody the untamed forces of nature, channeling energies that shape the world itself. Elementals resonate with the fundamental building blocks of existence, their very being a conduit for the wild, unfettered power that courses through the veins of the world.\n\n### Instruction:\nParadox: Anomalous\n\n### Response:\nDescriptor: Entities or artifacts branded as \"Anomalous\" defy conventional understanding, warping reality's fabric with their mere presence. They exude an unsettling aura of wrongness, their very existence a paradox that confounds logic and reason. Anomalous phenomena pulse with chaotic, unpredictable energies, challenging the fundamental laws of nature and leaving bewilderment and awe in their wake.\n\n### Instruction:\nParadox: Artistic\n\n### Response:\nDescriptor: Beings or objects infused with \"Artistic\" qualities exude creative energy and aesthetic brilliance. They pulsate with imaginative vitality, their very essence a canvas of expressive power. Artistic entities radiate an aura of inspired beauty, their existence a testament to the transformative nature of creative vision. They embody the harmonious interplay of form and function, their presence a vibrant celebration of artistic spirit.\n\n### Instruction:\nParadox: Mechanical\n\n### Response:\nDescriptor: Entities or items endowed with \"Mechanical\" properties are intricate, complex constructs that harness gears and levers, springs and pulleys. They exude a sense of calculated efficiency, their movement an intricate dance of cogs and wheels. Mechanical creations radiate a cool, precise energy, their existence a tribute to the masterful ingenuity of engineering. Their purpose, a symphony of mechanical ballet, is always clear and purposeful.\n\n### Instruction:\nParadox: {word}\n\n### Response:\nDescriptor:"
    request.prompt = prompt
    request.stop_sequence = ["###","Paradox:", "\n"]
    request.grammar = grammar
    request.grammar_string = grammar
    request.max_length = 200
    request.max_tokens = 200

    return request


async def doStuff():
    config.text_api = await apiconfig.set_api("text-default.json")
    await apiconfig.api_status_check(config.text_api["address"] + config.text_api["model"],
                                     headers=config.text_api["headers"])
    attribute_info = await read_attribute_data()
    for attribute in attribute_info.attributes:
        prompt = await getAttributeDescPrompt(attribute.name)
        gen_desc = await llmapi.send_to_llm(prompt)
        clean_text = re.sub(r'#|\n', '', gen_desc.results[0].text)
        attribute.desc = clean_text.strip()

    await write_attribute_data(attribute_info)


if __name__ == "__main__":
    asyncio.run(doStuff())