
import json
import math
import os
import time
from typing import Callable, Dict, List, Optional, Tuple, Union

from RePoE.poe_types import StatTranslation, TranslationCondition
from RePoE import mods, stat_translations, cluster_jewels

class Translator:
    # class for translating stats from the game to human readable format    

    def __init__(self, translation_table: List[StatTranslation] = stat_translations, translate_range: Optional[Callable[[Tuple[float, float]], str]] = None):
        self._translation_table = translation_table
        if translate_range is not None:
            self._translate_range = translate_range
        else:
            self._translate_range = self._translate_range_default


    @staticmethod
    def _translate_range_default(minmaxtuple: Tuple[float, float]) -> str:
        # default range translation function
        # for example, (10, 10) -> 10, (10, 20) -> (10-20)
        if minmaxtuple[0] == minmaxtuple[1]:
            return str(minmaxtuple[0])
        return f"({minmaxtuple[0]}-{minmaxtuple[1]})"

    @staticmethod
    def _get_min_max(stat: dict) -> Tuple[float, float]:
        # stats are not entirely consistent in how they are stored, so this function is used to get the min and max values
        if "value" in stat:
            return stat["value"], stat["value"]
        if "min" in stat and "max" in stat:
            return stat["min"], stat["max"]
        raise ValueError(f"Stat {stat} has no value or min/max")


    @staticmethod
    def _satisfies_conditions(conditions: List[TranslationCondition], min_max_range: List[Tuple[float, float]]) -> bool:
        # checks if the min_max_range satisfies the conditions
        # this will break down for mods like on ventor's gamble where the ranges go from negative to positive
        # and there is no canonical way to translate the stat for the entire range
        # in that case we will assume that the max value determines the translation
        
        for condition, min_max_tuple in zip(conditions, min_max_range):
            if condition == {} or condition.get("negated"): # honestly no idea what this does
                continue
            if "min" in  condition and min_max_tuple[1] < condition["min"]:
                return False
            if "max" in condition and min_max_tuple[1] > condition["max"]:
                return False
        return True
    

    @staticmethod
    def _apply_index_handler_to_value(value: float, handler:str):
        match handler:
            case "divide_by_twenty":
                return value / 20
            case "divide_by_fifteen_0dp":
                return value // 15
            case "times_one_point_five":
                return value * 1.5
            case "mod_value_to_item_class":
                return value
            case "weapon_tree_unique_base_type_name":
                # Reward from selling a crucible weapon with a weapon tree reward node
                return value
            case "display_indexable_skill":
                # Replica Dragonfang. No idea how to map values to skills
                return value
            case "locations_to_metres":
                return round(value / 10, 1)
            case "divide_by_one_thousand":
                return value / 1000
            case "tree_expansion_jewel_passive":
                # not sure how to handle this
                return value
            case "divide_by_twenty_then_double_0dp":
                return value // 10
            case "milliseconds_to_seconds_0dp":
                return value // 1000
            case "multiplicative_damage_modifier":
                # only one weird case so ignoring
                return value
            case "divide_by_ten_0dp":
                return value // 10
            case "divide_by_two_0dp":
                return value // 2
            case "divide_by_ten_1dp":
                return round(value / 10, 1)
            case "divide_by_ten_1dp_if_required":
                return round(value / 10, 1)
            case "divide_by_one_hundred_2dp":
                return round(value / 100, 2)
            case "per_minute_to_per_second_2dp_if_required":
                return round(value * 60, 2)
            case "30%_of_value":
                return value * 0.3
            case "deciseconds_to_seconds":
                return value / 10
            case "old_leech_permyriad":
                return value / 10000
            case "divide_by_four":
                return value / 4
            case "60%_of_value":
                return value * 0.6
            case "divide_by_one_hundred_2dp_if_required":
                return round(value / 100, 2)
            case "milliseconds_to_seconds":
                return value / 1000
            case "negate":
                return -value
            case "canonical_stat":
                return value
            case "divide_by_twelve":
                return value / 12
            case "times_twenty":
                return value * 20
            case "divide_by_six":
                return value / 6
            case "divide_by_fifty":
                return value / 50
            case "display_indexable_support":
                # Forbidden Shako. No idea how to map values to supports
                return value
            case "per_minute_to_per_second_0dp":
                return math.floor(value * 60)
            case "divide_by_one_hundred_and_negate":
                return -value / 100
            case "per_minute_to_per_second_1dp":
                return round(value * 60, 1)
            case "milliseconds_to_seconds_1dp":
                return round(value / 1000, 1)
            case "per_minute_to_per_second_2dp":
                return round(value * 60, 2)
            case "plus_two_hundred":
                return value + 200
            case "divide_by_three":
                return value / 3
            case "per_minute_to_per_second":
                return value * 60
            case "old_leech_percent":
                return value / 100
            case "divide_by_five":
                return value / 5
            case "milliseconds_to_seconds_2dp_if_required":
                return round(value / 1000, 2)
            case "divide_by_one_hundred":
                return value / 100
            case "affliction_reward_type":
                # delirium rewards. No idea how to map values to rewards
                return value
            case "passive_hash":
                # not sure how to handle this
                return value
            case "negate_and_double":
                return -value * 2
            case "double":
                return value * 2
            case _:
                raise ValueError(f"Unknown index handler {handler}")


    def translate_stats(self, stats: Union[List, Dict]) -> List[str]:
        translated_stats = []
        if isinstance(stats, list):
            stat_dict = {stat["id"]: self._get_min_max(stat) for stat in stats}
        elif isinstance(stats, dict):
            stat_dict = {stat_id: (value, value) for stat_id, value in stats.items()}
        else:
            raise ValueError(f"stats should be a list or dict, not {type(stats)}")
        
        untranslated_stats = set(stat_dict.keys())
        
        for translation in self._translation_table:
            if set(translation["ids"]).intersection(untranslated_stats) == set(translation["ids"]):
                for translation_candidate in translation["English"]:
                    if self._satisfies_conditions(translation_candidate["condition"], [stat_dict[stat_id] for stat_id in translation["ids"]]):
                        handled_values: List[List[float]] = [ ]	
                        for stat_id, handlers in zip(translation["ids"], translation_candidate["index_handlers"]):
                            handled_min_max_pair = []
                            for value in stat_dict[stat_id]:
                                for handler in handlers:
                                    value = self._apply_index_handler_to_value(value, handler)
                                handled_min_max_pair.append(value)
                            handled_values.append(handled_min_max_pair)
                        translated_stats.append(translation_candidate["string"].format(*[self._translate_range((values[0], values[1])) for values in handled_values]))
                        untranslated_stats -= set(translation["ids"])
                        break
            if not untranslated_stats:
                break
        if untranslated_stats:
            raise Warning(f"Untranslated stats: {untranslated_stats}")

        return translated_stats
