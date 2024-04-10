import json
from typing import List
import requests
import os
from RePoE import __DATA_PATH__


def save_file(file_name, data):
    with open(os.path.join(__DATA_PATH__, file_name + ".min.json"), "w") as f:
        f.write(json.dumps(data, separators=(",", ":"), sort_keys=True))
    with open(os.path.join(__DATA_PATH__, file_name + ".json"), "w") as f:
        f.write(json.dumps(data, indent=2, sort_keys=True))

def request_data_from_wiki(tables: list[str], fields: list[str], where: str="", join_on: str="", limit: int=500, offset: int = 0):
    url = "https://www.poewiki.net/w/api.php?action=cargoquery"
    url += f"&tables={','.join(tables)}"
    url += f"&fields={','.join(fields)}"
    if where:
        url += f"&where={where}"
    if join_on:
        url += f"&join_on={join_on}"
    url += f"&limit={limit}"
    url += f"&offset={offset}"
    url += "&format=json"
    response = requests.get(url)
    return [map_item(item["title"]) for item in response.json()["cargoquery"]]



def fix_explicit_stat_text(explicit_stat_text) -> List[List[str]]:
    # this will most likely break whenever the formatting in the wiki changes
    if not explicit_stat_text:
        return [[]]   
    explicit_stat_text = explicit_stat_text.replace("&lt;br /&gt;", "\n") # replace line breaks in a single stat
    values = explicit_stat_text.split("&lt;br&gt;") # separate stats
    value_lists = []
    for value in values:
        if "mw-customcollapsible-31&quot;&gt;&lt;td&gt;" in value: # indicates that there are multiple choices for a single stat
            value = value.split("mw-customcollapsible-31&quot;&gt;&lt;td&gt;")[1]
            value = value.replace("&lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;", "")
            value_lists.append(value.split("&lt;hr style=&quot;width: 20%&quot;&gt;"))
        elif "&lt;hr style=&quot;width: 20%&quot;&gt;" in value: # also indicates that there are multiple choices for a single stat
            value_lists.append(value.split("&lt;hr style=&quot;width: 20%&quot;&gt;"))
        else:
            value_lists.append([value]) # single choice for a stat
    return value_lists

def shorten_moster_metadata(metadata_id):
    return metadata_id.replace("Metadata/Monsters/", "")

def parameter_mapping(key, value):
    key = key.replace(" ", "_")
    if key in ["explicit_stat_text"]:   # html object that represents a list
        return fix_explicit_stat_text(value)
    if key in ["tags", "acquisition_tags"]:     # generic comma separated list
        return value.split(",") if value else []
    if key in ["is_drop_restricted", "drop_enabled"]:   # boolean
        return value == "1"
    if key in ["area_level", "tier"]:   # integer
        return int(value) if value else 0
    if key in ["boss_monster_ids", "drop_monsters"]:    # list of metadata that needs to be shortened
        if not value:
            return []
        return  [shorten_moster_metadata(v) for v in value.split(",")]
    if key in ["metadata_id"]:  # metadata that needs to be shortened
        return shorten_moster_metadata(value)
    return value  # value does not need to be converted

def map_item(item):
    return {key.replace(" ", "_"): parameter_mapping(key, value) for key, value in item.items()}


def fetch_unique_items(offset: int=0):
    limit = 500
    table = "items"
    fields = ["name", "class_id", "base_item", "is_drop_restricted", "drop_enabled", "drop_monsters", "explicit_stat_text", "acquisition_tags"]
    where = "rarity=%22Unique%22"
    return request_data_from_wiki([table], fields, where, "", limit, offset)

def fetch_areas(offset: int=0):
    limit = 500
    fields = ["name", "area_level", "boss_monster_ids", "tags", "id"]
    table = "areas"
    where = "is_map_area=1"
    return request_data_from_wiki([table], fields, where, "", limit, offset)

def fetch_unique_monsters(offset: int = 0):
    limit = 500
    fields = ["name", "metadata_id"]
    table = "monsters"
    where = "rarity=%22Unique%22"
    return request_data_from_wiki([table], fields, where, "", limit, offset)

def fetch_current_atlas_maps(offset: int = 0):
    limit = 500
    tables = ["maps", "areas"]
    fields = ["areas.name", "maps.tier"]
    where = "areas.is_map_area AND maps.tier > 0 AND maps.series=\"Necropolis\" AND areas.name != \"The Shaper's Realm\""
    join_on= "areas.id = maps.area_id"
    return request_data_from_wiki(tables, fields, where, join_on, limit, offset)


def fetch_all_unique_items():
    all_uniques = []
    offset = 0
    while True:
        new_uniques = fetch_unique_items(offset)
        offset += len(new_uniques)
        if len(new_uniques) == 0:
            break
        all_uniques.extend(new_uniques)
    save_file("unique_items", all_uniques)



def fetch_all_areas():
    all_areas = []
    offset = 0
    while True:
        new_areas = fetch_areas(offset)
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
    for areas in areas_by_name.values():
        condensed_area = areas[0]
        condensed_area["area_level"] = sorted({area["area_level"] for area in areas})
        condensed_areas.append(condensed_area)
    save_file("areas", condensed_areas)


def fetch_all_unique_monsters():
    all_bosses = []
    offset = 0
    while True:
        new_bosses = fetch_unique_monsters(offset)
        offset += len(new_bosses)
        if len(new_bosses) == 0:
            break
        all_bosses.extend(new_bosses)
    save_file("unique_monsters", {boss["metadata_id"]: boss["name"] for boss in all_bosses})



def fetch_all_atlas_maps(offset: int = 0):
    all_maps = []
    offset = 0
    while True:
        new_maps = fetch_current_atlas_maps(offset)
        offset += len(new_maps)
        if len(new_maps) == 0:
            break
        all_maps.extend(new_maps)
    save_file("atlas_maps", all_maps)


def fetch_wiki_data():
    fetch_all_unique_items()
    fetch_all_unique_monsters()
    fetch_all_areas()
    fetch_all_atlas_maps()


if __name__ == "__main__":
    fetch_wiki_data()
