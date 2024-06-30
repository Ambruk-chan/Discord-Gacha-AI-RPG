
from models import *
import json


async def read_character_data(display_name: str) -> Player:
    with open(f'{display_name}.json', 'r') as f:
        data = json.load(f)
        player = Player(**data)
    return player

async def write_character_data(player: Player):
    with open(f'{player.name}.json', 'w') as f:
        json.dump(player.__dict__, f)

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

async def read_ability_data(ability_name: str) -> Ability:
    with open(f'{ability_name}.json', 'r') as f:
        data = json.load(f)
        ability = Ability(**data)
    return ability

async def write_ability_data(ability: Ability):
    with open(f'{ability.name}.json', 'w') as f:
        json.dump(ability.__dict__, f)

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


        

def read_results_from_json(json_data: dict) -> Results:
    results = [ResultText(**result) for result in json_data['results']]
    return Results(results=results)
