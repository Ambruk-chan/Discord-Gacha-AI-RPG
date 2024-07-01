

from dataclasses import dataclass

@dataclass
class Stat:
    hp:int
    mp:int
    phys_atk:int
    phys_def:int
    men_atk:int
    men_def:int
    thaum_atk:int
    thaum_def:int
    pata_dmg:int
    pata_rate:float
    attributes: list[str]

@dataclass
class Equipment:
    name: str
    desc: str
    stat: Stat

@dataclass
class Player:
    name: str
    desc: str
    materials: list[str]
    stat: Stat
    weapon: Equipment
    armor: Equipment
    possession: Equipment
    power: Equipment

@dataclass
class Enemy:
    name: str
    desc: str
    materials: list[str]
    stat: Stat

@dataclass
class Encounter:
    name: str
    description: str
    dmg: int
    steal: int
    material: list[str]

@dataclass
class Dungeon:
    name:str
    floors:int
    enemies:list[Enemy]
    boss: Enemy
    encounter: list[Encounter]

@dataclass  
class Summon:
    name: str
    desc: str
    stat: Stat


# Okay, these are the stuff the AI will generate that isn't stored
@dataclass
class ResultText:
    text: str

@dataclass
class Results:
    results: list[ResultText]

@dataclass
class GenerationRequest:
    max_context_length: int
    max_length: int
    prompt: str
    quiet: bool
    rep_pen: float
    rep_pen_range: int
    rep_pen_slope: float
    temperature: float
    tfs: float
    top_a: float
    top_k: int
    top_p: float
    typical: float
    grammar: str = None
    grammar_string = None