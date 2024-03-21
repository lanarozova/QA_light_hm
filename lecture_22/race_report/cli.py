import argparse


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
        "--order", "-o",
        metavar="order",
        action="store",
        help="Order: 'ASC' - ascending, 'DESC' - descending",
        default="ASC",
        required=False
    )
    parser.add_argument(
        "--orderby",
        metavar="order by",
        action="store",
        help="Order by key: 'end' for end of race time, 'abbreviation', 'driver', 'team'",
        default='abbreviation',
        required=False
    )
    parser.add_argument(
        "--driver", "-d",
        metavar="driver",
        help="Show statistics about driver",
        default=False
    )
    return parser.parse_args()


if __name__ == "__main":
    args = parse_cli_args()
    folder = args.files
    order_asc = args.asc
    order_desc = args.desc
    driver = args.driver
