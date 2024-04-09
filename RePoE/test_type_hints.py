import dataclasses
import json
import os
import time
from typing import Dict, List, Optional


from dacite import from_dict, Config

from RePoE.dataclasse_types import *
# directory that this __init__ file lives in
__REPOE_DIR__, _ = os.path.split(__file__)

# full path to ./data
__DATA_PATH__ = os.path.join(__REPOE_DIR__, "data", "")


config = Config(strict=True)


def convert_json_to_dataclass(json_data: dict, dataclass: type):
    # return json_data
    fields = dataclasses.fields(dataclass)
    for key in json_data.keys():
        if key not in [field.name for field in fields]:
            raise ValueError(f"key {key} not in {dataclass}")

    return from_dict(data_class=dataclass, data=json_data, config=None)


def load_json(json_file_path: str, dataclass: Optional[type] = None, format: Format = Format.DICT):
    file_path = __DATA_PATH__ + f"{json_file_path}"
    with open(file_path) as json_data:
        try:
            data = json.load(json_data)
            if dataclass:
                if format == Format.LIST:
                    return [convert_json_to_dataclass(v, dataclass) for v in data]
                elif format == Format.DICT:
                    return {k: convert_json_to_dataclass(v, dataclass) for k, v in data.items()}
            else:
                return data
        except json.decoder.JSONDecodeError:
            print(
                f"Warning: {json_file_path} failed to decode json \n Recommended to execute run_parser.py to fix")


t = time.time()
active_skill_types: List[str] = load_json("active_skill_types.min.json")
base_items: Dict[str, BaseItem] = load_json(
    "base_items.min.json", BaseItem, Format.DICT)
characters: List[Character] = load_json(
    "characters.min.json", Character, Format.LIST)
crafting_bench_options: List[CraftingBenchOption] = load_json(
    "crafting_bench_options.min.json", CraftingBenchOption, Format.LIST)
default_monster_stats: Dict[str, DefaultMonsterStats] = load_json(
    "default_monster_stats.min.json", DefaultMonsterStats, Format.DICT)
essences: Dict[str, Essences] = load_json(
    "essences.min.json", Essences, Format.DICT)
flavour: Dict[str, str] = load_json("flavour.min.json")
fossils: Dict[str, Fossil] = load_json("fossils.min.json", Fossil, Format.DICT)
gems: Dict[str, Gem] = load_json("gems.min.json", Gem, Format.DICT)
gem_tags: Dict[str, Optional[str]] = load_json("gem_tags.min.json")
item_classes: Dict[str, ItemClass] = load_json(
    "item_classes.min.json", ItemClass, Format.DICT)
mods: Dict[str, Mod] = load_json(
    "mods.min.json", Mod, Format.DICT)
mod_types: Dict[str, ModTypes] = load_json(
    "mod_types.min.json", ModTypes, Format.DICT)
stats = load_json("stats.min.json", Stat, Format.DICT)
stat_translations: List[StatTranslation] = load_json(
    "stat_translations.min.json", StatTranslation, Format.LIST)
tags = load_json("tags.min.json")
cluster_jewels = load_json("cluster_jewels.min.json",
                           ClusterJewel, Format.DICT)
cluster_jewel_notables = load_json(
    "cluster_jewel_notables.min.json", ClusterJewelNotable, Format.LIST)
cost_types = load_json("cost_types.min.json", CostType, Format.DICT)
print(time.time()-t)


def _get_all_json_files(base_path=__DATA_PATH__):
    """get all json files in /data"""
    json_files = [
        pos_json
        for pos_json in os.listdir(base_path)
        if pos_json.endswith(".json") and not pos_json.endswith(".min.json")
    ]
    return json_files


def _assert_all_json_files_accounted_for(base_path=__DATA_PATH__, globals=globals()):
    json_files = _get_all_json_files(base_path=base_path)
    for json_file in json_files:
        json_file_stripped, _, _ = json_file.partition(".json")

        assert json_file_stripped in globals, f"the following json file needs to be added to load: {json_file_stripped}"


# _assert_all_json_files_accounted_for()

if __name__ == "__main__":
    condition_keys = set()
    for mod in stat_translations:
        for translation in mod.English:
            for handler in translation.index_handlers:
                for h in handler:
                    condition_keys.add(h)
    print(condition_keys)
