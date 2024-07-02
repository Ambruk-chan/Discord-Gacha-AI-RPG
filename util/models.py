from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin


@dataclass
class Stat(DataClassJsonMixin):
    hp: int = 0
    phys_atk: int = 0
    phys_def: int = 0
    men_atk: int = 0
    men_def: int = 0
    thaum_atk: int = 0
    thaum_def: int = 0
    pata_dmg: int = 0
    pata_rate: float = 0.0
    attributes: list = field(default_factory=list)


@dataclass
class Equipment(DataClassJsonMixin):
    name: str = ""
    desc: str = ""
    stat: Stat = field(default_factory=Stat)


@dataclass
class Player(DataClassJsonMixin):
    name: str = ""
    desc: str = ""
    materials: list[str] = field(default_factory=list)
    stat: Stat = field(default_factory=Stat)
    weapon: Equipment = field(default_factory=Equipment)
    armor: Equipment = field(default_factory=Equipment)
    possession: Equipment = field(default_factory=Equipment)
    power: Equipment = field(default_factory=Equipment)


@dataclass
class Enemy(DataClassJsonMixin):
    name: str
    desc: str
    materials: list[str]
    stat: Stat


@dataclass
class Encounter(DataClassJsonMixin):
    name: str
    description: str
    dmg: int
    steal: int
    material: list[str]


@dataclass
class Dungeon(DataClassJsonMixin):
    name: str
    floors: int
    enemies: list[Enemy]
    boss: Enemy
    encounter: list[Encounter]


@dataclass
class Summon(DataClassJsonMixin):
    name: str
    desc: str
    stat: Stat


@dataclass
class Attribute(DataClassJsonMixin):
    name: str
    desc: str
    type: str
    rare: int
    stat: str


@dataclass
class AttributeType(DataClassJsonMixin):
    name: str
    desc: str


@dataclass
class AttributeModifier(DataClassJsonMixin):
    name: str
    atk: int
    res: int
    hp: int


@dataclass
class AttributeInfo(DataClassJsonMixin):
    attributes: list[Attribute]
    types: list[AttributeType]
    modifier: list[AttributeModifier]


# Okay, these are the stuff the AI will generate that isn't stored
@dataclass
class Result(DataClassJsonMixin):
    text: str
    finish_reason: str


@dataclass
class Response(DataClassJsonMixin):
    results: list[Result] = field(default_factory=list)


@dataclass
class GenerationRequest(DataClassJsonMixin):
    prompt = ""
    stop_sequence = []
    add_bos_token = True
    ban_eos_token = True
    do_sample = False
    max_length = 1024
    max_tokens = 1024
    max_context_length = 8192
    genamt = 1095
    temp = 1.20
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
    ]
    grammar: str | None = None
    grammar_string: str | None = None
