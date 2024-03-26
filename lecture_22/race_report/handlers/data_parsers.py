from pathlib import PureWindowsPath
from collections import defaultdict
import re


def parse_log_file_data(log_file_path: PureWindowsPath) -> dict:
    start_or_end = "start" if re.search(r"start", log_file_path.name) else "end"
    data = defaultdict(dict)
    with open(log_file_path) as file:
        for line in file.readlines():
            line = line.strip()
            abbr = re.search(r"[A-Z]{3}", line).group()
            d_t = re.search(r"[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}", line).group()
            data[abbr][start_or_end] = d_t
    return data


def parse_abbreviations(file_path: PureWindowsPath) -> dict:
    abbreviations = {}
    with open(file_path) as file:
        for line in file.readlines():
            abbr = line.strip().split("_")
            abbreviations[abbr[0]] = abbr
    return abbreviations
