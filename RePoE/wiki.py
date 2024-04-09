import json
from typing import List
import requests
import os
from RePoE import __DATA_PATH__

base_url = "https://www.poewiki.net/w/api.php?action=cargoquery"

def save_file(file_name, data):
    with open(os.path.join(__DATA_PATH__, file_name), "w") as f:
        f.write(json.dumps(data, separators=(",", ":"), sort_keys=True))

def fix_explicit_stat_text(explicit_stat_text) -> List[List[str]]:
    # this will most likely break whenever the formatting in the wiki changes
    if not explicit_stat_text:
        return [[]]   

    values = explicit_stat_text.split("&lt;br&gt;")
    value_list = []
    for value in values:
        if "mw-customcollapsible-31&quot;&gt;&lt;td&gt;" in value:
            value = value.split("mw-customcollapsible-31&quot;&gt;&lt;td&gt;")[1]
            value = value.replace("&lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;", "")
            value_list.append(value.split("&lt;hr style=&quot;width: 20%&quot;&gt;"))
        elif "&lt;hr style=&quot;width: 20%&quot;&gt;" in value:
            value_list.append(value.split("&lt;hr style=&quot;width: 20%&quot;&gt;"))
        else:
            value_list.append([value])

    return value_list

def shorten_moster_metadata(metadata_id):
    return metadata_id.replace("Metadata/Monsters/", "")

def parameter_mapping(key, value):
    key = key.replace(" ", "_")
    if key in ["explicit_stat_text"]:
        return fix_explicit_stat_text(value)
    if key in ["tags"]:
        return value.split(",") if value else []
    if key in ["is_drop_restricted", "drop_enabled"]:
        return value == "1"
    if key in ["area_level"]:
        return int(value) if value else 0
    if key in ["boss_monster_ids", "drop_monsters"]:
        if not value:
            return []
        return  [shorten_moster_metadata(v) for v in value.split(",")]
    if key in ["metadata_id"]:
        return shorten_moster_metadata(value)
    return value

def map_item(item):
    return {key.replace(" ", "_"): parameter_mapping(key, value) for key, value in item.items()}


def get_uniques(offset: int=0):
    limit = 500
    table = "items"
    fields = ["name", "class_id", "base_item", "is_drop_restricted", "drop_enabled", "drop_monsters", "explicit_stat_text"]

    url = f"https://www.poewiki.net/w/api.php?action=cargoquery&tables={table}&fields={','.join(fields)}&where=rarity=%22Unique%22&limit={limit}&format=json&offset={offset}"
    response = requests.get(url)

    return [map_item(item["title"]) for item in response.json()["cargoquery"]]

def fetch_all_unique_items():
    all_uniques = []
    offset = 0
    while True:
        new_uniques = get_uniques(offset)
        offset += len(new_uniques)
        if len(new_uniques) == 0:
            break
        all_uniques.extend(new_uniques)
    save_file("unique_items.min.json", all_uniques)

def get_areas(offset: int=0):
    limit = 500
    fields = ["name", "area_level", "boss_monster_ids", "tags"]
    table = "areas"
    url = f"{base_url}&tables={table}%2C+&fields={','.join(fields)}&where=is_map_area=1&limit={limit}&offset={offset}&format=json"
    response = requests.get(url)
    return [map_item(item["title"]) for item in response.json()["cargoquery"]]


def fetch_all_areas():
    all_areas = []
    offset = 0
    while True:
        new_areas = get_areas(offset)
        offset += len(new_areas)
        if len(new_areas) == 0:
            break
        all_areas.extend(new_areas)
    

    areas_by_name = {}
    for area in all_areas:
        if area["name"] not in areas_by_name:
            areas_by_name[area["name"]] = []
        areas_by_name[area["name"]].append(area)
    
    condensed_areas = []
    for name, areas in areas_by_name.items():
        condensed_area = {
            "name": name,
            "area_levels": sorted({area["area_level"] for area in areas}),
            "boss_monster_ids": areas[0]["boss_monster_ids"],
            "tags": areas[0]["tags"]
        }
        condensed_areas.append(condensed_area)
    save_file("areas.min.json", condensed_areas)

def get_bosses(offset: int = 0):
    limit = 500
    fields = ["name", "metadata_id"]
    table = "monsters"
    url = f"{base_url}&tables={table}&fields={','.join(fields)}&where=rarity=%22Unique%22&limit={limit}&offset={offset}&format=json"
    response = requests.get(url)
    return [map_item(item["title"]) for item in response.json()["cargoquery"]]

def fetch_all_unique_monsters():
    all_bosses = []
    offset = 0
    while True:
        new_bosses = get_bosses(offset)
        offset += len(new_bosses)
        if len(new_bosses) == 0:
            break
        all_bosses.extend(new_bosses)
    save_file("unique_monsters.min.json", all_bosses)


def fetch_wiki_data():
    fetch_all_unique_items()
    fetch_all_unique_monsters()
    fetch_all_areas()


if __name__ == "__main__":
    fetch_wiki_data()
