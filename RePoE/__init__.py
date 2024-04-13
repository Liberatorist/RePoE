import json
import os
from typing import Dict, List, Optional

from RePoE.poe_types import *
# directory that this __init__ file lives in
__REPOE_DIR__, _ = os.path.split(__file__)

# full path to ./data
__DATA_PATH__ = os.path.join(__REPOE_DIR__, "data", "")


def load_json(json_file_path: str):
    file_path = __DATA_PATH__ + f"{json_file_path}"
    with open(file_path) as json_data:
        try:
            return json.load(json_data)
        except json.decoder.JSONDecodeError:
            raise Exception(
                f"Warning: {json_file_path} failed to decode json \n Recommended to reinstall RePoE")


active_skill_types: List[str] = load_json("active_skill_types.min.json")
base_items: Dict[str, BaseItem] = load_json("base_items.min.json")
characters: List[Character] = load_json("characters.min.json")
crafting_bench_options: List[CraftingBenchOption] = load_json(
    "crafting_bench_options.min.json")
default_monster_stats: Dict[str, DefaultMonsterStats] = load_json(
    "default_monster_stats.min.json")
essences: Dict[str, Essences] = load_json("essences.min.json")
flavour: Dict[str, str] = load_json("flavour.min.json")
fossils: Dict[str, Fossil] = load_json("fossils.min.json")
gems: Dict[str, Gem] = load_json("gems.min.json")
gem_tags: Dict[str, Optional[str]] = load_json("gem_tags.min.json")
item_classes: Dict[str, ItemClass] = load_json("item_classes.min.json")
mods: Dict[str, Mod] = load_json("mods.min.json")
mod_types: Dict[str, ModTypes] = load_json("mod_types.min.json")
stats: Dict[str, Stat] = load_json("stats.min.json")
stat_translations: List[StatTranslation] = load_json(
    "stat_translations.min.json")
tags: List[str] = load_json("tags.min.json")
cluster_jewels: Dict[str, ClusterJewel] = load_json("cluster_jewels.min.json")
cluster_jewel_notables: List[ClusterJewelNotable] = load_json(
    "cluster_jewel_notables.min.json")
cost_types: Dict[str, CostType] = load_json("cost_types.min.json")
skill_tree: SkillTree = load_json("skill_tree.min.json")
atlas_tree: AtlasTree = load_json("atlas_tree.min.json")
