

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