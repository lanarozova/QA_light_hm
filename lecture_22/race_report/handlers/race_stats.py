from collections import defaultdict
import datetime
from prettytable.colortable import ColorTable, Theme


def get_race_info(
        abbreviations: dict,
        start_race_data: dict,
        end_race_data: dict,
        driver: str
) -> dict[dict]:

    race_info = defaultdict(dict)

    def set_race_data_to_driver(driver_abbr):
        race_info[driver_abbr]["abbr"] = abbreviations[driver_abbr]
        start = datetime.datetime.fromisoformat(start_race_data[driver_abbr]["start"])
        end = datetime.datetime.fromisoformat(end_race_data[driver_abbr]["end"])
        if end < start:
            end, start = start, end
        race_info[driver_abbr]["result"] = str(end - start)[:-3]
        race_info[driver_abbr]["date"] = datetime.datetime.strftime(start, "%Y.%m.%d")
        race_info[driver_abbr]["start"] = datetime.datetime.strftime(start, "%H:%M:%S.%f")[:-3]
        race_info[driver_abbr]["end"] = datetime.datetime.strftime(end, "%H:%M:%S.%f")[:-3]

    try:
        if driver:
            driver = driver.strip().upper()
            if driver not in abbreviations:
                raise ValueError("Such driver doesn't exist in racing data")
            else:
                set_race_data_to_driver(driver)
        else:
            for key in abbreviations:
                set_race_data_to_driver(key)
    except ValueError as error:
        print(error)
    return race_info


def get_table_data(race_info: dict):
    fields = ["Abbreviation", "Name", "Team", "Date", "Start", "End", "Result"]
    data = []
    for key in race_info:
        row = race_info[key]["abbr"]
        for name in ["date", "start", "end", "result"]:
            row.append(race_info[key][name])
        data.append(row)
    return fields, sorted(data, key=lambda item: item[-1])


def create_table(
        fields: list[str],
        table_data: list[list],
        order_by: str,
        order: str
) -> ColorTable:

    order = order.strip().upper()
    order_by = order_by.strip().lower().capitalize()
    try:
        if order_by not in fields:
            raise ValueError(f"sort_by option '{order_by}' is not found")
        if order not in ["ASC", "DESC"]:
            raise ValueError(f"sort_order option '{order}' is not found")
        reverse = False if order == "ASC" else True

        table = ColorTable(
            theme=Theme(
                default_color="36",
                vertical_color="37",
                horizontal_color="37",
                junction_color="36"
            )
        )
        fields.insert(0, "Place")
        table.field_names = fields
        if order_by != "Abbreviation":
            table.sortby = order_by
        table.reversesort = reverse
        iterator = iter(range(1, len(table_data) + 1))
        for row in table_data:
            row.insert(0, next(iterator))
            table.add_row(row)
        return table
    except ValueError as error:
        print(error)
