from collections import defaultdict
import datetime
# from termcolor import colored
from prettytable import PrettyTable


# print colored('hello', 'red'), colored('world', 'green')
#

def get_all_race_info(abbreviations: dict, start_race_data: dict, end_race_data: dict) -> dict[dict]:
    all_race_info = defaultdict(dict)
    for key in abbreviations:
        all_race_info[key]["abbr"] = abbreviations[key]
        start = start_race_data[key]["start"]
        end = end_race_data[key]["end"]
        all_race_info[key]["start"] = start
        all_race_info[key]["end"] = end
        all_race_info[key]["result"] = str(
            datetime.datetime.fromisoformat(end) - datetime.datetime.fromisoformat(start)
        )
    return all_race_info


def get_table_data(all_race_info: dict):
    fields = ["abbreviation", "name", "team", "start", "end", "result"]
    data = []
    for key in all_race_info:
        row = all_race_info[key]["abbr"]
        for name in ["start", "end", "result"]:
            row.append(all_race_info[key][name])
        data.append(row)
    return fields, data


def sort_table_data(fields: list[str], table_data: list[list], sort_by: str, reverse: bool = False):
    sort_by_keys = fields
    index = sort_by_keys.index(sort_by) if sort_by in sort_by_keys else -1
    sorted_table_data = sorted(table_data, key=lambda item: item[index], reverse=reverse)
    return sorted_table_data


def create_table(fields: list[str], table_data: list[list]):
    table = PrettyTable()
    table.field_names = [field.capitalize() for field in fields]
    for row in table_data:
        table.add_row(row)
    return table








