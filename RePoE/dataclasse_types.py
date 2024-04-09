from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Literal, Optional, Union


class Format(Enum):
    DICT = 0
    LIST = 1


@dataclass
class Requirements:
    strength: int
    dexterity: int
    intelligence: int
    level: int


@dataclass
class BaseItemProperty:
    min: int
    max: int


@dataclass
class VisualIdentity:
    dds_file: str
    id: str


@dataclass
class FlaskBuff:
    id: str
    stats: Dict[str, int]


@dataclass
class BaseItem:
    name: str
    item_class: str
    inventory_width: int
    inventory_height: int
    drop_level: int
    implicits: list[str]
    tags: list[str]
    visual_identity: VisualIdentity
    properties: Dict[str, Union[int, str, BaseItemProperty]]
    release_state: str
    requirements: Optional[Requirements] = None
    grants_buff: Optional[FlaskBuff] = None


@dataclass
class Unarmed:
    attack_time: float
    min_physical_damage: int
    max_physical_damage: int
    range: int


@dataclass
class CharacterBaseStats:
    life: int
    mana: int
    strength: int
    dexterity: int
    intelligence: int
    unarmed: Unarmed


@dataclass
class Character:
    metadata_id: str
    integer_id: int
    name: str
    base_stats: CharacterBaseStats


@dataclass
class CraftingBenchAction:
    add_explicit_mod: Optional[Union[str, int, bool]] = None
    add_enchant_mod: Optional[Union[str, int, bool]] = None
    link_sockets: Optional[Union[str, int, bool]] = None
    color_sockets: Optional[Union[str, int, bool]] = None
    change_socket_count: Optional[Union[str, int, bool]] = None
    remove_crafted_mods: Optional[Union[str, int, bool]] = None
    remove_enchantments: Optional[Union[str, int, bool]] = None


@dataclass
class CraftingBenchOption:
    master: str
    bench_tier: int
    item_classes: List[str]
    cost: Dict[str, int]
    actions: CraftingBenchAction


@dataclass
class DefaultMonsterStats:
    physical_damage: float
    evasion: int
    accuracy: int
    life: int
    ally_life: int
    armour: int


@dataclass
class EssenceMods:
    Amulet: Optional[str] = None
    OneHandAxe: Optional[str] = None
    TwoHandAxe: Optional[str] = None
    OneHandMace: Optional[str] = None
    TwoHandMace: Optional[str] = None
    OneHandSword: Optional[str] = None
    TwoHandSword: Optional[str] = None
    Bow: Optional[str] = None
    Claw: Optional[str] = None
    Dagger: Optional[str] = None
    Sceptre: Optional[str] = None
    Staff: Optional[str] = None
    Wand: Optional[str] = None
    Shield: Optional[str] = None
    Helmet: Optional[str] = None
    BodyArmour: Optional[str] = None
    Gloves: Optional[str] = None
    Boots: Optional[str] = None
    Ring: Optional[str] = None
    Belt: Optional[str] = None
    Quiver: Optional[str] = None
    ThrustingOneHandSword: Optional[str] = None


@dataclass
class EssenceType:
    tier: int
    is_corruption_only: bool


@dataclass
class Essences:
    name: str
    spawn_level_min: int
    spawn_level_max: int
    level: int
    item_level_restriction: Optional[int]
    type: EssenceType
    mods: EssenceMods


@dataclass
class Weight:
    tag: str
    weight: int


@dataclass
class Fossil:
    name: str
    added_mods: List[str]
    forced_mods: List[str]
    negative_mod_weights: List[Weight]
    positive_mod_weights: List[Weight]
    forbidden_tags: List[str]
    allowed_tags: List[str]
    corrupted_essence_chance: int
    mirrors: bool
    changes_quality: bool
    rolls_lucky: bool
    rolls_white_sockets: bool
    sell_price_mods: List[str]
    descriptions: List[str]
    blocked_descriptions: List[str]


@dataclass
class SupportGem:
    added_types: List[str]
    allowed_types: List[str]
    excluded_types: List[str]
    letter: str
    supports_gems_only: bool


@dataclass
class GemQualityStat:
    id: str
    value: int


@dataclass
class GemStat:
    id: Optional[str]
    value: Optional[int]


@dataclass
class PerLevelStat:
    value: Optional[int]


@dataclass
class Reservations:
    mana_flat: Optional[int]
    life_flat: Optional[int]
    mana_percent: Optional[float]
    life_percent: Optional[float]


@dataclass
class Cost:
    Mana: Optional[int]
    Life: Optional[int]
    ES: Optional[int]
    ManaPerMinute: Optional[int]
    ManaPercent: Optional[int]


@dataclass
class Vaal:
    souls: int
    stored_uses: int


@dataclass
class GemStatic:
    costs: Optional[Cost]
    attack_speed_multiplier: Optional[float]
    quality_stats: Optional[List[GemQualityStat]]
    stat_requirements: Optional[Dict[Literal["dex", "int", "str"], int]]
    stats: Optional[List[Optional[GemStat]]]
    cost_multiplier: Optional[int]
    cooldown: Optional[int]
    stored_uses: Optional[int]
    damage_effectiveness: Optional[float]
    crit_chance: Optional[float]
    damage_multiplier: Optional[float]
    reservations: Optional[Reservations]
    required_level: Optional[float]
    vaal: Optional[Vaal]
    cooldown_bypass_type: Optional[str]


@dataclass
class GemBaseItem:
    id: str
    display_name: str
    release_state: str


@dataclass
class ActiveSkill:
    id: str
    display_name: str
    description: str
    types: List[str]
    weapon_restrictions: List[str]
    is_skill_totem: bool
    is_manually_casted: bool
    stat_conversions: Dict[str, str]
    skill_totem_life_multiplier: Optional[float]
    minion_types: Optional[List[str]] = None


@dataclass
class Gem:
    is_support: bool
    tags: Optional[List[str]]
    stat_translation_file: str
    per_level: Dict[str, GemStatic]
    static: GemStatic
    base_item: Optional[GemBaseItem] = None
    active_skill: Optional[ActiveSkill] = None
    support_gem: Optional[SupportGem] = None
    secondary_granted_effect: Optional[str] = None
    cast_time: Optional[float] = None


@dataclass
class ItemClass:
    name: str


@dataclass
class ModStat:
    id: str
    min: float
    max: float


@dataclass
class Mod:
    required_level: int
    stats: List[ModStat]
    domain: str
    name: str
    type: str
    generation_type: str
    groups: List[str]
    spawn_weights: List[Weight]
    generation_weights: List[Weight]
    grants_effects: List[dict]
    is_essence_only: bool
    adds_tags: List[str]
    implicit_tags: List[str]


@dataclass
class ModTypes:
    sell_price_types: List[str]


@dataclass
class StatAlias:
    when_in_main_hand: Optional[str]
    when_in_off_hand: Optional[str]


@dataclass
class Stat:
    alias: StatAlias
    is_aliased: bool
    is_local: bool


@dataclass
class TranslationCondition:
    max: Optional[int]
    min: Optional[int]
    negated: Optional[bool]


@dataclass
class TranslationInstance:
    condition: List[TranslationCondition]
    format: List[Literal["ignore", "#", "+#"]]
    index_handlers: List[List[str]]
    string: str


@dataclass
class StatTranslation:
    English: List[TranslationInstance]
    ids: List[str]
    hidden: Optional[bool] = None


@dataclass
class ClusterJewelNotable:
    id: str
    jewel_stat: str
    name: str


@dataclass
class ClusterJewelPassiveSkill:
    id: str
    name: str
    stats: Dict[str, int]
    tag: str


@dataclass
class ClusterJewel:
    max_skills: int
    min_skills: int
    name: str
    notable_indices: List[int]
    passive_skills: List[ClusterJewelPassiveSkill]
    size: str
    small_indices: List[int]
    socket_indices: List[int]
    total_indices: int


@dataclass
class CostType:
    format_text: str
    stat: str
