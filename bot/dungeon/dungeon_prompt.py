from util.models import *


def create_dungeon_grammar():
    grammar = "\nroot ::= \"[Dungeon: \" [^\\r\\n\\x0b\\x0c\\x85\\u2028\\u2029]+ \"]\\n[Event 1: \" enc \"[Event 2: \"bat \"[Event 3: \" enc \"[Event 4: \" bat \"[Event 5: \" enc \"[Event 6: \" boss\n\nenc ::= \"Encounter\\nDescription:\" paragraph \"]\\n\\n\"\n\nbat ::= \"Battle\\nEnemy: \"paragraph\"\\nDescription:\" paragraph \"]\\n\\n\"\n\nboss::= \"Boss Battle\\nEnemy: \"paragraph\"\\nDescription:\" paragraph \"]###\"\n\nnum ::= (\"1\"|\"2\"|\"3\"|\"4\"|\"5\"|\"6\"|\"7\"|\"8\"|\"9\")\n\nparagraph ::= [^\\r\\n\\x0b\\x0c\\x85\\u2028\\u2029\\]]+"

    return grammar


def dungeon_creation_prompt(catalyst):
    request = GenerationRequest()
    grammar = create_dungeon_grammar()
    prompt = f"Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\nBased on the catalyst given, Dungeon Creator will create a dungeon for a text RPG Game.\n\nImportant Things Of Note:\n\n- The dungeon name\n- Six events, alternating between encounters and battles\n- Descriptions for each event\nEnemy names for the battle events\n- The sixth event (Boss Battle) must feature a sexy/cute/beautiful monster girl \n\n- Event description must be less than 2 sentences\n### Instruction:\nUser: Catalyst: [Aquamarine Shard]\n\n### Response:\nDungeon Creator: [Dungeon: The Abyssal Trench]\n[Event 1: Encounter\nDescription: A shimmering portal opens at the edge of a cliff, revealing a vast underwater cavern. The air ripples as it meets the water's surface, and bioluminescent algae cast an eerie blue glow throughout the chamber.]\n\n[Event 2: Battle\nEnemy: Colossal Kraken Spawn\nDescription: A monstrous creature with tentacles as thick as tree trunks and a body the size of a small ship. Its skin glistens with a slimy, iridescent sheen, and rows of sharp teeth line its beak-like mouth. The kraken spawn's eyes glow with an otherworldly blue light, matching the aquamarine shard embedded in its forehead.]\n\n[Event 3: Encounter\nDescription: A field of giant, luminous anemones covers the cavern floor. Their tendrils sway hypnotically in the water currents, concealing treasures and dangers alike within their colorful fronds.]\n\n[Event 4: Battle\nEnemy: Coral Golem\nDescription: A hulking humanoid figure composed entirely of living coral and sea creatures. Its body constantly shifts and changes as fish, crabs, and other marine life move within its structure. The golem's fists are studded with sharp pieces of coral, and a pulsing aquamarine light emanates from its chest.]\n\n[Event 5: Encounter\nDescription: You enter a grotto filled with ancient, submerged ruins. Ornate pillars and crumbling statues hint at a long-lost civilization. Strange, glowing glyphs on the walls seem to react to your presence, pulsing with aquamarine light.]\n\n[Event 6: Monster Girl Boss Battle\nEnemy: Nereid Queen Coralline\nDescription: A regal figure with the upper body of a voluptous woman and the lower body of an octopus glides into view. Her skin shimmers with an opalescent blue hue, and her hair flows like living seaweed. Coralline wears a crown of aquamarine crystals that amplify her formidable water manipulation abilities. Despite her fearsome and alluring appearance, her eyes betray a deep intelligence and a hint of sorrow. The Nereid Queen commands the sea itself, but seems bound to this place by some ancient magic.]\n\n### Instruction:\nUser: Catalyst: {catalyst}\n\n### Response(descriptive, creative):\nDungeon Creator:"
    request.prompt = prompt
    request.stop_sequence = ["<END>"]
    request.grammar = grammar
    request.grammar_string = grammar
    request.max_length = 1024
    request.max_tokens = 1024
    return request


def enemy_intro_prompt(action:DungeonAction):
    request = GenerationRequest()
    grammar = "TODO HERE" #TODO
    enemy = action.dungeon.events[action.floor].event
    prompt = f"Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\nBased on the creature description written by User, Dungeon Narrator will write down an introduction/dramatic appearance of the creature.\n### Instruction:\nUser: Name: [Spirit of the Prairie]\nDescription: [A colossal, four-legged creature with an antlered head and a mane of lightning. Its body shimmers with energy, and it wields the power of the storm. The Spirit of the Prairie has roamed these lands for centuries, protecting the land and its people from those who would seek to tame it.]\n\n### Response:\nDungeon Narrator: [As you crest the hill, the air crackles with electricity, and the wind whips into a frenzy. Suddenly, the prairie before you comes alive. A massive form materializes from shimmering air, its four legs sending tremors through the earth with each step. An enormous antlered head rises, crowned by a mane that dances with blue-white lightning.\n\nThe Spirit of the Prairie fixes you with ancient eyes that flash like thunderbolts. Its translucent body pulses with barely contained energy, and storm clouds gather overhead at its silent command. You feel the weight of centuries in its gaze, a primal force of nature incarnate. The air hums with power as the spirit paws the ground, ready to defend its domain against any who would threaten the sanctity of these wild lands.]\n\n### Instruction:\nUser: Name: [Queen Jungle Oracle]\nDescription:[A beautiful woman with skin the color of mahogany, she wears leaves as a crown and carries a staff of ancient wood. Her eyes glow with wisdom and power, and she summons vines and animals to defend her domain. The Oracle's voice echoes through the jungle as she challenges you to understand the balance of nature.]\n\n### Response:\nDungeon Narrator: [The dense foliage parts as if by an unseen hand, revealing a clearing bathed in ethereal green light. At its center stands a regal figure, her mahogany skin gleaming like polished wood. Atop her head sits a crown of vibrant leaves, swaying gently despite the stillness of the air. In her grasp, an ancient staff pulses with primal energy, its surface etched with symbols of forgotten lore.\n\nThe Queen Jungle Oracle's eyes lock onto you, glowing with otherworldly knowledge. As she speaks, her voice reverberates through the trees, carried by unseen spirits. Vines slither from the undergrowth at her command, coiling protectively around her feet. The jungle itself seems to breathe with her, leaves rustling and animals emerging from hiding. With a gesture, she beckons you forward, challenging you to prove your worth and your understanding of nature's delicate balance.]\n\n### Instruction:\nUser: Name: [{enemy.name}]\nDescription:[{enemy.description}]\n\n### Response(descriptive, creative):\nDungeon Narrator: "
    request.prompt = prompt
    request.stop_sequence = ["<END>"]
    request.grammar = grammar
    request.grammar_string = grammar
    request.max_length = 1024
    request.max_tokens = 1024
    return request

# TODO: PWOMPT ENGWEENIWING
def dungeon_starting_prompt(player, dungeon):

    return None
