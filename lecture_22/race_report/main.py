from pathlib import PureWindowsPath
import os


from handlers.validators import (validate_log_file_format,
                                 validate_folder,
                                 validate_abbreviations_file_format)

from handlers.data_parsers import (parse_abbreviations,
                                   parse_log_file_data)

from handlers.race_stats import (get_race_info,
                                 get_table_data,
                                 create_table)


def get_absolute_path(folder, file_name) -> PureWindowsPath:
    filepath = os.path.abspath("main.py")
    abs_path = PureWindowsPath(filepath).parent.joinpath(folder + "\\" + file_name)
    return abs_path


def main(
        folder: str,
        order_by: str = "result",
        order: str = "ASC",
        driver: str = "") -> None:

    if validate_folder(folder):
        abbr_file = get_absolute_path(folder, "abbreviations.txt")
        start_log = get_absolute_path(folder, "start.log")
        end_log = get_absolute_path(folder, "end.log")

        if all(
                [
                    validate_log_file_format(start_log),
                    validate_log_file_format(end_log),
                    validate_abbreviations_file_format(abbr_file)
                ]
        ):
            start_data = parse_log_file_data(start_log)
            end_data = parse_log_file_data(end_log)
            abbreviations = parse_abbreviations(abbr_file)
            race_info = get_race_info(abbreviations, start_data, end_data, driver)

            fields, table_data = get_table_data(race_info)
            print(create_table(fields, table_data, order_by, order))


if __name__ == "__main__":
    main("racing_data", order="desc")
