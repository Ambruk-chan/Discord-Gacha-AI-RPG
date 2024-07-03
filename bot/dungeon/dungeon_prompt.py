from util.models import *


def create_dungeon_grammar():
    grammar = "\nroot ::= \"[Dungeon: \" [^\\r\\n\\x0b\\x0c\\x85\\u2028\\u2029]+ \"]\\n[Event 1: \" enc \"[Event 2: \"bat \"[Event 3: \" enc \"[Event 4: \" bat \"[Event 5: \" enc \"[Event 6: \" boss\n\nenc ::= \"Encounter\\nDescription:\" paragraph \"]\\n\\n\"\n\nbat ::= \"Battle\\nEnemy: \"paragraph\"\\nDescription:\" paragraph \"]\\n\\n\"\n\nboss::= \"Boss Battle\\nEnemy: \"paragraph\"\\nDescription:\" paragraph \"]###\"\n\nnum ::= (\"1\"|\"2\"|\"3\"|\"4\"|\"5\"|\"6\"|\"7\"|\"8\"|\"9\")\n\nparagraph ::= [^\\r\\n\\x0b\\x0c\\x85\\u2028\\u2029\\]]+"

    return grammar
def dungeon_creation_prompt(catalyst, player_data:Player):
    request = GenerationRequest()
    grammar = create_dungeon_grammar()
    prompt = f"Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\nBased on the catalyst given by {player_data.name}, Dungeon Creator will create a dungeon for {player_data.name}.\n\nImportant Things Of Note:\n\n- The dungeon name\n- Six events, alternating between encounters and battles\n- Descriptions for each event\nEnemy names for the battle events\n- The sixth event (Boss Battle) must feature a sexy/cute/beautiful monster girl \n\n- Event description must be less than 2 sentences\n### Instruction:\n{player_data.name}: Catalyst: [Aquamarine Shard]\n\n### Response:\nDungeon Creator: [Dungeon: The Abyssal Trench]\n[Event 1: Encounter\nDescription: A shimmering portal opens at the edge of a cliff, revealing a vast underwater cavern. The air ripples as it meets the water's surface, and bioluminescent algae cast an eerie blue glow throughout the chamber.]\n\n[Event 2: Battle\nEnemy: Colossal Kraken Spawn\nDescription: A monstrous creature with tentacles as thick as tree trunks and a body the size of a small ship. Its skin glistens with a slimy, iridescent sheen, and rows of sharp teeth line its beak-like mouth. The kraken spawn's eyes glow with an otherworldly blue light, matching the aquamarine shard embedded in its forehead.]\n\n[Event 3: Encounter\nDescription: A field of giant, luminous anemones covers the cavern floor. Their tendrils sway hypnotically in the water currents, concealing treasures and dangers alike within their colorful fronds.]\n\n[Event 4: Battle\nEnemy: Coral Golem\nDescription: A hulking humanoid figure composed entirely of living coral and sea creatures. Its body constantly shifts and changes as fish, crabs, and other marine life move within its structure. The golem's fists are studded with sharp pieces of coral, and a pulsing aquamarine light emanates from its chest.]\n\n[Event 5: Encounter\nDescription: You enter a grotto filled with ancient, submerged ruins. Ornate pillars and crumbling statues hint at a long-lost civilization. Strange, glowing glyphs on the walls seem to react to your presence, pulsing with aquamarine light.]\n\n[Event 6: Monster Girl Boss Battle\nEnemy: Nereid Queen Coralline\nDescription: A regal figure with the upper body of a voluptous woman and the lower body of an octopus glides into view. Her skin shimmers with an opalescent blue hue, and her hair flows like living seaweed. Coralline wears a crown of aquamarine crystals that amplify her formidable water manipulation abilities. Despite her fearsome and alluring appearance, her eyes betray a deep intelligence and a hint of sorrow. The Nereid Queen commands the sea itself, but seems bound to this place by some ancient magic.]\n\n### Instruction:\n{player_data.name}: Catalyst: {catalyst}\n\n### Response(descriptive, creative):\nDungeon Creator:"
    request.prompt = prompt
    request.stop_sequence = ["<END>"]
    request.grammar = grammar
    request.grammar_string = grammar
    request.max_length = 1024
    request.max_tokens = 1024


    return request


def enemy_intro_prompt(action):
    return None


def enemy_action_prompt(action,battle_result):
    return None


def enemy_defeat_prompt(action):
    return None


def epilogue_prompt(dungeon, history):
    return None
