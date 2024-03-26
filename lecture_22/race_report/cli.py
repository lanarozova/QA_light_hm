import argparse

from main import main


def parse_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="CLI Interface for Race report app",
        usage="%(prog)s cli.py '--files '<folder path>' '[--asc | --desc]' [--driver <driver name>]'",
        description="Show report about Monaco race_report"
    )
    parser.add_argument(
        "--files", "-f",
        metavar="files",
        type=str,
        help="Path to folder with txt files",
        required=True
    )
    parser.add_argument(
        "--order_by", "-ob",
        metavar="order by",
        action="store",
        help="Order by key: 'abbreviation', 'name', 'team', 'start', 'end', 'result'. "
             "Default sort key is 'abbreviation'",
        default='abbreviation',
        required=False
    )
    parser.add_argument(
        "--order", "-o",
        metavar="order",
        action="store",
        help="Order: 'ASC' - ascending, 'DESC' - descending",
        default="ASC",
        required=False
    )
    parser.add_argument(
        "--driver", "-d",
        metavar="driver",
        help="Show information about a single driver",
        default=False
    )
    arguments = parser.parse_args()
    return arguments


if __name__ == "__main__":
    args = parse_cli_args()
    folder = args.files
    order_by = args.order_by
    order = args.order
    driver = args.driver

    main(folder, order_by=order_by, order=order, driver=driver)
