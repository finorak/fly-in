import sys

from parser.get_args import get_args
from parser.parsing import Parser

try:
    from src.app import App
except Exception as e:
    print(e)
    sys.exit(1)


def main() -> None:
    """Entry point of the program
    """
    args = get_args()
    parser = Parser(args.input)
    app = App(parser)
    app.run()


if __name__ == "__main__":
    main()
