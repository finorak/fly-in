from parser.get_args import get_args
from parser.parsing import Parser
from src.app import App


def main() -> None:
    """Entry point of the program
    """
    args = get_args()
    parser = Parser(args.input)
    app = App(parser, args.visual)
    app._init()
    app.run()


if __name__ == "__main__":
    main()
