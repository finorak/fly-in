from argparse import ArgumentParser, Namespace


def get_args() -> Namespace:
    """Using argparse, we can add
    another argument without modifying
    to many codes, just adding a few lines
    of codes.
    """
    parser: ArgumentParser = ArgumentParser(
            description="A drone simulation app",
            usage="uv run python -m codes --input [file]")
    parser.add_argument(
            "--input", type=str, help="Map file",
            default="maps/easy/01_linear_path.txt"
            )
    parser.add_argument(
            "--visual", type=bool, help="To show or not",
            default=False
            )
    return parser.parse_args()
