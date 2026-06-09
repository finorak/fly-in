import sys
from parser.parsing import Parser
from parser.get_args import get_args

try:
    from src.app import App
except Exception as e:
    print(e)
    sys.exit(1)


def main() -> None:
    """Entry point of the program
    """
    args = get_args()
    parser = Parser(args.input_file)
    app = App(parser)
    app.run()


if __name__ == "__main__":
    main()
