from dataclasses import asdict
import os
from util.models import *
import json

def read_character_data(player_name: str) -> Player:
    file_path = f'./data/player/{player_name}.json'
    full_path = os.path.abspath(file_path)
    print(f"Reading from file: {full_path}")

    try:
        with open(file_path, 'r') as f:
            json_data = f.read()

        # Use the from_json method provided by dataclasses_json
        player = Player.from_json(json_data)
        return player
    except FileNotFoundError:
        print(f"No data found for player: {player_name}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON data for player: {player_name}")
        return None


def write_character_data(player: Player):
    file_path = f'./data/player/{player.name}.json'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    full_path = os.path.abspath(file_path)
    print(f"Full file path: {full_path}")

    with open(file_path, 'w') as f:
        f.write(player.to_json(indent=2))


async def read_dungeon_data(dungeon_name: str) -> Dungeon:
    with open(f'{dungeon_name}.json', 'r') as f:
        data = json.load(f)
        dungeon = Dungeon(**data)
    return dungeon


async def write_dungeon_data(dungeon: Dungeon):
    with open(f'{dungeon.name}.json', 'w') as f:
        json.dump(dungeon.__dict__, f)


async def read_enemy_data(enemy_name: str) -> Enemy:
    with open(f'{enemy_name}.json', 'r') as f:
        data = json.load(f)
        enemy = Enemy(**data)
    return enemy


async def write_enemy_data(enemy: Enemy):
    with open(f'{enemy.name}.json', 'w') as f:
        json.dump(enemy.__dict__, f)


async def read_encounter_data(encounter_name: str) -> Encounter:
    with open(f'{encounter_name}.json', 'r') as f:
        data = json.load(f)
        encounter = Encounter(**data)
    return encounter


async def write_encounter_data(encounter: Encounter):
    with open(f'{encounter.name}.json', 'w') as f:
        json.dump(encounter.__dict__, f)


async def read_summon_data(summon_name: str) -> Summon:
    with open(f'{summon_name}.json', 'r') as f:
        data = json.load(f)
        summon = Summon(**data)
    return summon


async def write_summon_data(summon: Summon):
    with open(f'{summon.name}.json', 'w') as f:
        json.dump(summon.__dict__, f)


async def read_attribute_data() -> AttributeInfo:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, '..', 'data', 'global', 'attributes.json')

    # Read the JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)
    attributes = [Attribute(**attr) for attr in data['AttributeInfo']['attributes']]
    types = [AttributeType(**type_) for type_ in data['AttributeInfo']['types']]
    stats = [AttributeModifier(**stat_) for stat_ in data['AttributeInfo']['stat']]
    return AttributeInfo(attributes=attributes, types=types, modifier=stats)


async def write_attribute_data(attr_info: AttributeInfo) -> str:
    return json.dumps({"AttributeInfo": asdict(attr_info)}, indent=2)


async def get_player_list():
    player_list = []
    return player_list


def read_results_from_json(json_data) -> Response:
    response = Response()
    for result in json_data['results']:
        response.results.append(Result(
            text=result['text'],
            finish_reason=result['finish_reason']
        ))

    return response
