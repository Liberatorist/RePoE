from RePoE.parser import Parser_Module
from RePoE.parser.util import call_with_default_args, write_json


def _convert_mods(row):
    class_to_key = {
        "Amulet": "Amulet_ModsKey",
        "Belt": "Belt_ModsKey",
        "BodyArmour": "BodyArmour_ModsKey",
        "Boots": "Boots_ModsKey",
        "Bow": "Bow_ModsKey",
        "Claw": "Claw_ModsKey",
        "Dagger": "Dagger_ModsKey",
        "Gloves": "Gloves_ModsKey",
        "Helmet": "Helmet_ModsKey",
        "OneHandAxe": "OneHandAxe_ModsKey",
        "OneHandMace": "OneHandMace_ModsKey",
        "OneHandSword": "OneHandSword_ModsKey",
        "Quiver": "Display_Quiver_ModsKey",
        "Ring": "Ring_ModsKey",
        "Sceptre": "Sceptre_ModsKey",
        "Shield": "Shield_ModsKey",
        "Staff": "Staff_ModsKey",
        "ThrustingOneHandSword": "OneHandThrustingSword_ModsKey",
        "TwoHandAxe": "TwoHandAxe_ModsKey",
        "TwoHandMace": "TwoHandMace_ModsKey",
        "TwoHandSword": "TwoHandSword_ModsKey",
        "Wand": "Wand_ModsKey",
    }
    return {item_class: row[key]["Id"] for item_class, key in class_to_key.items() if row[key] is not None}


def get_essence_min_drop_level(row):
    # kind of a hack, but I cant seem to find where the max level is stored now
    if not row["DropLevel"]:
        return 0
    return row["DropLevel"][0]


class essences(Parser_Module):
    @staticmethod
    def write(file_system, data_path, relational_reader, translation_file_cache, ot_file_cache):
        essences = {
            row["BaseItemTypesKey"]["Id"]: {
                "name": row["BaseItemTypesKey"]["Name"],
                "spawn_level_min": get_essence_min_drop_level(row),
                "spawn_level_max": 0,
                "level": row["Level"],
                "item_level_restriction": row["ItemLevelRestriction"] if row["ItemLevelRestriction"] > 0 else None,
                "type": {
                    "tier": row["EssenceTypeKey"]["EssenceType"],
                    "is_corruption_only": row["EssenceTypeKey"]["IsCorruptedEssence"],
                },
                "mods": _convert_mods(row),
            }
            for row in relational_reader["Essences.dat64"]
        }
        write_json(essences, data_path, "essences")


if __name__ == "__main__":
    call_with_default_args(essences.write)
