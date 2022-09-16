import argparse

from pathlib import Path

def parse_args() -> argparse.Namespace:
    """
    Parse the command line arguments
    """
    parser = argparse.ArgumentParser(description='Simulates a Badgerloop Race')
    parser.add_argument("-c", "--config", type=Path, default=Path("configs/default.json"))
    parser.add_argument("-d", "--dump_template", action="store_true")


if __name__ == "__main__":
    parse_args()
