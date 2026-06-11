from parser.get_args import get_args
from parser.parsing import Parser
from src.app import App

# TODO: ADD A TRY EXCEPT FOR THIS BLOCK
# WE REMOVED THEM ONLY FOR DEVELOPEMENT PURPOSE


def main() -> None:
    """Entry point of the program
    """
    args = get_args()
    parser = Parser(args.input)
    app = App(parser, args.visual)
    app.run()


if __name__ == "__main__":
    main()
