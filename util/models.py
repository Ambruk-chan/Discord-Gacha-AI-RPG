

from dataclasses import dataclass

@dataclass
class Ability:
    name: str
    description: str

    phys_dmg: int
    men_dmg: int
    thaum_dmg: int
    pata_dmg: int

    phys_heal: int
    men_heal: int
    thaum_heal: int
    pata_heal: int
    
    phys_buff: int
    men_buff: int
    thaum_buff: int
    pata_buff: int

    cost: int
    
@dataclass
class Player:
    name: str
    hp: int
    mp: int
    materials: list[str]
    phys:int
    men:int
    thaum:int
    pata:int
    crit_dmg:int
    crit_rate:int
    abilities: list[Ability]

@dataclass
class Enemy:
    name: str
    hp: int
    mp: int
    materials: list[str]
    phys:int
    men:int
    thaum:int
    pata:int
    crit_dmg:int
    crit_rate:int
    abilities: list[Ability]

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
    hp: int
    mp: int
    rarity: int
    phys:int
    men:int
    thaum:int
    pata:int
    crit_dmg:int
    crit_rate:int
    abilities: list[Ability]


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

class envelope:
    text: str
    thread: str #??