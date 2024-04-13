from typing import Dict, List, Literal, NotRequired, TypedDict, Union


class Requirements(TypedDict):
    strength: int
    dexterity: int
    intelligence: int
    level: int


class BaseItemProperty(TypedDict):
    min: int
    max: int


class VisualIdentity(TypedDict):
    dds_file: str
    id: str


class FlaskBuff(TypedDict):
    id: str
    stats: Dict[str, int]


class BaseItem(TypedDict):
    name: str
    item_class: str
    inventory_width: int
    inventory_height: int
    drop_level: int
    implicits: list[str]
    tags: list[str]
    visual_identity: VisualIdentity
    properties: Dict[str, dict]
    release_state: str
    requirements: NotRequired[Requirements]
    grants_buff: NotRequired[FlaskBuff]


class WikiBaseItem(TypedDict):
    name: str
    item_class: str
    inventory_width: int
    inventory_height: int
    drop_level: int
    implicits: list[str]
    tags: list[str]
    visual_identity: VisualIdentity
    properties: Dict[str, BaseItemProperty]
    release_state: str
    requirements: NotRequired[Requirements]
    grants_buff: NotRequired[FlaskBuff]


class Unarmed(TypedDict):
    attack_time: float
    min_physical_damage: int
    max_physical_damage: int
    range: int


class CharacterBaseStats(TypedDict):
    life: int
    mana: int
    strength: int
    dexterity: int
    intelligence: int
    unarmed: Unarmed


class Character(TypedDict):
    metadata_id: str
    integer_id: int
    name: str
    base_stats: CharacterBaseStats


class CraftingBenchAction(TypedDict):
    add_explicit_mod: NotRequired[Union[str, int, bool]]
    add_enchant_mod: NotRequired[Union[str, int, bool]]
    link_sockets: NotRequired[Union[str, int, bool]]
    color_sockets: NotRequired[Union[str, int, bool]]
    change_socket_count: NotRequired[Union[str, int, bool]]
    remove_crafted_mods: NotRequired[Union[str, int, bool]]
    remove_enchantments: NotRequired[Union[str, int, bool]]


class CraftingBenchOption(TypedDict):
    master: str
    bench_tier: int
    item_classes: List[str]
    cost: Dict[str, int]
    actions: CraftingBenchAction


class DefaultMonsterStats(TypedDict):
    physical_damage: float
    evasion: int
    accuracy: int
    life: int
    ally_life: int
    armour: int


class EssenceMods(TypedDict):
    Amulet: NotRequired[str]
    OneHandAxe: NotRequired[str]
    TwoHandAxe: NotRequired[str]
    OneHandMace: NotRequired[str]
    TwoHandMace: NotRequired[str]
    OneHandSword: NotRequired[str]
    TwoHandSword: NotRequired[str]
    Bow: NotRequired[str]
    Claw: NotRequired[str]
    Dagger: NotRequired[str]
    Sceptre: NotRequired[str]
    Staff: NotRequired[str]
    Wand: NotRequired[str]
    Shield: NotRequired[str]
    Helmet: NotRequired[str]
    BodyArmour: NotRequired[str]
    Gloves: NotRequired[str]
    Boots: NotRequired[str]
    Ring: NotRequired[str]
    Belt: NotRequired[str]
    Quiver: NotRequired[str]
    ThrustingOneHandSword: NotRequired[str]


class EssenceType(TypedDict):
    tier: int
    is_corruption_only: bool


class Essences(TypedDict):
    name: str
    spawn_level_min: int
    spawn_level_max: int
    level: int
    item_level_restriction: NotRequired[int]
    type: EssenceType
    mods: EssenceMods


class Weight(TypedDict):
    tag: str
    weight: int


class Fossil(TypedDict):
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


class SupportGem(TypedDict):
    added_types: List[str]
    allowed_types: List[str]
    excluded_types: List[str]
    letter: str
    supports_gems_only: bool


class PerLevelStat(TypedDict):
    value: NotRequired[int]


class Reservations(TypedDict):
    mana_flat: NotRequired[int]
    life_flat: NotRequired[int]
    mana_percent: NotRequired[float]
    life_percent: NotRequired[float]


class Cost(TypedDict):
    Mana: NotRequired[int]
    Life: NotRequired[int]
    ES: NotRequired[int]
    ManaPerMinute: NotRequired[int]
    ManaPercent: NotRequired[int]


class Vaal(TypedDict):
    souls: int
    stored_uses: int


class GemStatic(TypedDict):
    costs: NotRequired[Cost]
    attack_speed_multiplier: NotRequired[float]
    quality_stats: NotRequired[Dict[str, int]]
    stat_requirements: NotRequired[Dict[Literal["dex", "int", "str"], int]]
    stats: NotRequired[Dict[str, int]]
    cost_multiplier: NotRequired[int]
    cooldown: NotRequired[int]
    stored_uses: NotRequired[int]
    damage_effectiveness: NotRequired[float]
    crit_chance: NotRequired[float]
    damage_multiplier: NotRequired[float]
    reservations: NotRequired[Reservations]
    required_level: NotRequired[float]
    vaal: NotRequired[Vaal]
    cooldown_bypass_type: NotRequired[str]


class GemBaseItem(TypedDict):
    id: str
    display_name: str
    release_state: str


class ActiveSkill(TypedDict):
    id: str
    display_name: str
    description: str
    types: List[str]
    weapon_restrictions: List[str]
    is_skill_totem: bool
    is_manually_casted: bool
    stat_conversions: Dict[str, str]
    skill_totem_life_multiplier: NotRequired[float]
    minion_types: NotRequired[List[str]]


class Gem(TypedDict):
    is_support: bool
    tags: NotRequired[List[str]]
    stat_translation_file: str
    per_level: Dict[str, GemStatic]
    static: GemStatic
    base_item: NotRequired[GemBaseItem]
    active_skill: NotRequired[ActiveSkill]
    support_gem: NotRequired[SupportGem]
    secondary_granted_effect: NotRequired[str]
    cast_time: NotRequired[float]


class ItemClass(TypedDict):
    name: str


class ModStat(TypedDict):
    id: str
    min: float
    max: float


class Mod(TypedDict):
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


class ModTypes(TypedDict):
    sell_price_types: List[str]


class StatAlias(TypedDict):
    when_in_main_hand: NotRequired[str]
    when_in_off_hand: NotRequired[str]


class Stat(TypedDict):
    alias: StatAlias
    is_aliased: bool
    is_local: bool


class TranslationCondition(TypedDict):
    max: NotRequired[int]
    min: NotRequired[int]
    negated: NotRequired[bool]


class TranslationInstance(TypedDict):
    condition: List[TranslationCondition]
    format: List[Literal["ignore", "#", "+#"]]
    index_handlers: List[List[str]]
    string: str


class StatTranslation(TypedDict):
    English: List[TranslationInstance]
    ids: List[str]
    hidden: NotRequired[bool]


class ClusterJewelNotable(TypedDict):
    id: str
    jewel_stat: str
    name: str


class Rect(TypedDict):
    height: int
    width: int
    x: int
    y: int


class ClusterJewelPassiveSkill(TypedDict):
    name: str
    stats: Dict[str, int]
    tag: str


class ClusterJewel(TypedDict):
    max_skills: int
    min_skills: int
    name: str
    notable_indices: List[int]
    passive_skills: Dict[str, ClusterJewelPassiveSkill]
    size: str
    small_indices: List[int]
    socket_indices: List[int]
    total_indices: int


class CostType(TypedDict):
    format_text: str
    stat: str


class Ascendancy(TypedDict):
    flavourText: str
    flavourTextColour: str
    flavourTextRect: Rect
    id: str
    name: str


class PoEClass(TypedDict):
    ascendancies: List[Ascendancy]
    base_dex: int
    base_int: int
    base_str: int
    name: str


class SkillTreeConstants(TypedDict):
    PSSCentreInnerRadius: int
    characterAttributes: Dict[str, int]
    classes: Dict[str, int]
    orbitRadii: List[int]
    skillsPerOrbit: List[int]


class SkillTreeExtraImage(TypedDict):
    image: str
    x: float
    y: float


class SkillTreeBackground(TypedDict):
    image: str
    isHalfImage: bool


class SkillTreeGroup(TypedDict):
    background: SkillTreeBackground
    nodes: List[str]
    orbits: List[int]
    x: float
    y: float


class MasteryEffect(TypedDict):
    effect: int
    stats: List[str]
    reminderText: NotRequired[List[str]]


class SkillTreeNode(TypedDict):
    group: int
    icon: str
    in_: List[str]
    out: List[str]
    name: str
    orbit: int
    orbitIndex: int
    out: List[str]
    reminderText: List[str]
    skill: int
    stats: List[str]
    activeIcon: NotRequired[str]
    activeEffectImage: NotRequired[str]
    inactiveIcon: NotRequired[str]
    recipe: NotRequired[List[str]]
    isNotable: NotRequired[bool]
    isBlighted: NotRequired[bool]
    isKeystone: NotRequired[bool]
    isJewelSocket: NotRequired[bool]
    isProxy: NotRequired[bool]
    isMastery: NotRequired[bool]
    isAscendancyStart: NotRequired[bool]
    masteryEffects: NotRequired[List[MasteryEffect]]
    grantedPassivePoints: NotRequired[int]
    grantedIntelligence: NotRequired[int]
    grantedDexterity: NotRequired[int]
    grantedStrength: NotRequired[int]
    classStartIndex: NotRequired[int]
    ascendancyName: NotRequired[str]
    ascendancyClassName: NotRequired[str]
    ascendancyClass: NotRequired[str]
    isMultipleChoice: NotRequired[bool]
    isMultipleChoiceOption: NotRequired[bool]
    expansionJewel: NotRequired[bool]
    grantedSkills: NotRequired[List[str]]
    grantedNotable: NotRequired[str]
    isJewelSocketActive: NotRequired[bool]
    activeIcon: NotRequired[str]


class SkillTreePoints(TypedDict):
    ascendancyPoints: int
    totalPoints: int


class SkillTree(TypedDict):
    alternate_ascendancies: List[Ascendancy]
    classes: List[PoEClass]
    constants: SkillTreeConstants
    extra_images: Dict[str, SkillTreeExtraImage]
    groups: Dict[str, SkillTreeGroup]
    imageZoomLevels: List[float]
    jewelSlots: List[int]
    max_x: int
    max_y: int
    min_x: int
    min_y: int
    nodes: Dict[str, SkillTreeNode]
    points: SkillTreePoints
    sprites: dict
    tree: Literal["default"]


class AtlasTree(TypedDict):
    constants: SkillTreeConstants
    groups: Dict[str, SkillTreeGroup]
    imageZoomLevels: List[float]
    max_x: int
    max_y: int
    min_x: int
    min_y: int
    nodes: Dict[str, SkillTreeNode]
    points: SkillTreePoints
    sprites: dict
    tree: Literal["Atlas"]


class UniqueItem(TypedDict):
    name: str
    class_id: str
    base_item: str
    is_drop_restricted: bool
    drop_enabled: bool
    drop_monsters: List[str]
    explicit_stat_text: List[str]
    acquisition_tags: List[str]


class Area(TypedDict):
    name: str
    area_levels: List[int]
    boss_monster_ids: List[str]
    tags: List[str]


class Map(TypedDict):
    name: str
    tier: int
