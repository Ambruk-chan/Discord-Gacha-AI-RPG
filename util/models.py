from dataclasses import dataclass, field
from enum import Enum
from typing import Union

import discord
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Stat:
    hp: int = 0
    max_hp = 0
    phys_atk: int = 0
    phys_def: int = 0
    phys_res: int = 0
    men_atk: int = 0
    men_def: int = 0
    men_res: int = 0
    thaum_atk: int = 0
    thaum_def: int = 0
    thaum_res: int = 0
    pata_dmg: int = 0
    pata_rate: float = 0.0
    attributes: list = field(default_factory=list)


@dataclass
class Entity:
    name: str = ""
    desc: str = ""
    stat: Stat | None = None


@dataclass_json
@dataclass
class Equipment:
    name: str = ""
    desc: str = ""
    stat: Stat = field(default_factory=Stat)


@dataclass_json
@dataclass
class DungeonProgress:
    dungeon_name: str = ""
    position: int = 0
    situation: str | None = None


@dataclass_json
@dataclass
class Player:
    name: str = ""
    desc: str = ""
    materials: list[str] = field(default_factory=list)
    stat: Stat = field(default_factory=Stat)
    weapon: Equipment = field(default_factory=Equipment)
    armor: Equipment = field(default_factory=Equipment)
    possession: Equipment = field(default_factory=Equipment)
    power: Equipment = field(default_factory=Equipment)
    progress: DungeonProgress = field(default_factory=DungeonProgress)
    turn: bool = False


@dataclass_json
@dataclass
class Choice:
    desc: str = ""
    materials: list[str] = field(default_factory=list)
    type: str = ""
    action: str = ""


@dataclass_json
@dataclass
class Enemy:
    name: str = ""
    desc: str = ""
    materials: list[str] = field(default_factory=list)
    stat: Stat = field(default_factory=Stat)
    turn: int = 0


@dataclass_json
@dataclass
class Encounter: # Well fuck, guess I do need to name my encounter...
    name: str # WELL FUCK! I HAVE TO RECREATE THE DUNGEON CREATION SYSTEM!!!!
    description: str
    choices: list[Choice] = field(default_factory=list)


@dataclass_json
@dataclass
class Event:
    event: Union[Encounter, Enemy]


@dataclass_json
@dataclass
class Dungeon:
    name: str = ""
    events: list[Event] = field(default_factory=list)
    thread: int = 0


@dataclass_json
@dataclass
class Summon:
    name: str
    desc: str
    stat: Stat


@dataclass_json
@dataclass
class Attribute:
    name: str
    desc: str
    type: str
    rare: int
    stat: str


@dataclass_json
@dataclass
class AttributeType:
    name: str
    desc: str


@dataclass_json
@dataclass
class AttributeModifier:
    name: str
    atk: int
    res: int
    hp: int


@dataclass_json
@dataclass
class AttributeInfo:
    attributes: list[Attribute]
    types: list[AttributeType]
    modifier: list[AttributeModifier]


# Okay, these are the stuff the AI will generate that isn't stored
@dataclass_json
@dataclass
class Result:
    text: str
    finish_reason: str


@dataclass_json
@dataclass
class Response:
    results: list[Result] = field(default_factory=list)


@dataclass_json
@dataclass
class GenerationRequest:
    prompt = ""
    stop_sequence = []
    add_bos_token = True
    ban_eos_token = True
    do_sample = False
    max_length = 1024
    max_tokens = 1024
    max_context_length = 8192
    genamt = 1095
    temp = 1.20,
    top_k = 0
    top_p = 0.75
    top_a = 0
    typical = 1
    tfs = 1.0
    rep_pen = 1
    rep_pen_range = 0
    rep_pen_slope = 0.9
    use_default_badwordsids = True
    early_stopping = True
    sampler_order = [
        6,
        0,
        1,
        3,
        4,
        2,
        5
    ],
    grammar = None,
    grammar_string = None


# Never Will Json

@dataclass
class CalculationResult:
    name: str
    desc: str
    stat: Stat


@dataclass
class CharacterCreationQueueItem:
    interaction: discord.Interaction
    description: str


@dataclass
class DungeonCreationQueueItem:
    interaction: discord.Interaction
    material: str = "Tutorial Book"

@dataclass
class DungeonEnterQueueItem:
    interaction: discord.Interaction
    player: Summon|Player
    dungeon_name: str = ""



class ActionType(Enum):
    ATTACK = "Attack"
    DEFEND = "Defend"
    FLEE = "Flee"


class DamageType(Enum):
    PHYSICAL = "Physical"
    MENTAL = "Mental"
    THAUMATURGIC = "Thaumaturgic"


@dataclass
class BattleAction:
    action: ActionType
    type: DamageType
    quip: str


@dataclass
class EncounterAction:
    choice: str = ""
    material: list = field(default_factory=list)
    quip: str = ""


@dataclass
class PassAction:
    quip: str = ""


@dataclass
class DungeonActionQueueItem:
    interaction: discord.Interaction
    action: BattleAction | EncounterAction | PassAction | None


@dataclass
class DungeonRecord:
    type: str = ""
    meta: str = ""
    story: str = ""


@dataclass
class DungeonHistory:
    thread_id: int | None = None
    user: str | None = None
    player: Entity | None = None
    enemy: Entity | None = None
    records: list[DungeonRecord] | None = None
    dungeon: Dungeon | None = None
    floor: int | None = None
    materials: list | None = None


@dataclass
class DungeonAction:
    history: DungeonHistory | None = None
    action: BattleAction | EncounterAction | None = None
    floor: int | None = None
    result: str | None = None


@dataclass
class BattleResult:
    attacker: Stat
    target: Stat
    meta_info: str


@dataclass
class ActionResult:
    stat_change:Stat | None = None
    material_change: list | None = None
    meta_info:str|None = None
