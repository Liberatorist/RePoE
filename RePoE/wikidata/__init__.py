import json
import os
from typing import Dict, List

from RePoE.poe_types import *
# directory that this __init__ file lives in
__REPOE_DIR__, _ = os.path.split(__file__)

# full path to ./data
__DATA_PATH__ = os.path.join(__REPOE_DIR__, "wikidata", "")


def load_json(json_file_path: str):
    file_path = __DATA_PATH__ + f"{json_file_path}"
    with open(file_path) as json_data:
        try:
            return json.load(json_data)
        except json.decoder.JSONDecodeError:
            raise Exception(
                f"Warning: {json_file_path} failed to decode json \n Recommended to reinstall RePoE")


unique_items: List[UniqueItem] = load_json("unique_items.min.json")
unique_monsters: Dict[str, str] = load_json("unique_monsters.min.json")
areas: List[Area] = load_json("areas.min.json")
maps: List[Map] = load_json("atlas_maps.min.json")
base_items: Dict[str, WikiBaseItem] = load_json("base_items_wiki.min.json")
