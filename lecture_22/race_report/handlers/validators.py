import re
import datetime
import os
from pathlib import PurePath, PureWindowsPath


def validate_folder(folder: str) -> bool:
    try:
        if not os.path.isdir(folder):
            raise FileExistsError
    except FileExistsError as error:
        print(error)
        return False
    return True


def validate_date(date_str: str) -> bool:
    try:
        if not datetime.date.fromisoformat(date_str):
            raise ValueError
    except ValueError:
        print("Incorrect data format in the log file, should be YYYY-MM-DD")
        return False
    return True


def validate_time(time_str: str) -> bool:
    try:
        if not datetime.time.fromisoformat(time_str):
            raise ValueError
    except ValueError:
        print("Incorrect time format in the log file, should be HH:MM:SS:sss")
        return False
    return True


def validate_log_file_format(log_file: PureWindowsPath) -> bool:
    try:
        with open(log_file) as file:
            line = file.readline().strip()
            match_line = re.match(
                r"^[A-Z]{3}[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}$",
                line
            )
            match_date = re.search(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", line)
            match_time = re.search(r"[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}", line)
            if not match_line:
                raise ValueError("Incorrect log file text format.")
            if not validate_date(match_date.group()):
                return False
            if not validate_time(match_time.group()):
                return False

    except (UnicodeError, ValueError) as error:
        print(error)
        return False
    return True


def validate_abbreviations_file_format(file_path: PureWindowsPath) -> bool:
    try:
        with open(file_path) as file:
            line = file.readline().strip()
            match = re.match(r"[A-Z]{3}_[A-Z][a-z]+\s[A-Z][a-z]+_[A-Z\s]+", line)
            if not match:
                raise ValueError
    except UnicodeDecodeError as error:
        print(error)
        return False
    except ValueError as error:
        print("Abbreviations file is not in correct format."
              "Should be 'ABBR_Firstname Lastname_COMMAND NAME'")
        return False
    return True


if __name__ == "__main__":
    filepath = os.path.abspath("validators.py")
    logfile_name = r"racing_data\start.log"
    abbr_file = r"racing_data\abbreviations.txt"
    p = PureWindowsPath(filepath).parents[1].joinpath(logfile_name)
    abbr_p = PureWindowsPath(filepath).parents[1].joinpath(abbr_file)
    print(p)
    date = "2018-05-24"
    time = "12:02:58.9t5"
    log_f = "SVF2018-05-24_12:02:58.917"
    print(validate_log_file_format(p))

    print(validate_abbreviations_file_format(abbr_p))





