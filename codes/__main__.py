import sys

import pygame
from algorithm.find_path import solve
from parser.parsing import Parser
from src.app import App
from utils.helper import get_args


def main() -> None:
    """Entry point of the program
    """
    args = get_args()
    parser = Parser(args.input)
    app = App(parser, args.visual)
    app._init()
    solve(app.data.drones, app.data.cells, app.data.dict_connections)
    app.run()


if __name__ == "__main__":
    try:
        main()
    except pygame.error as e:
        print(e, file=sys.stderr)
    # TODO: REMOVE THIS BEFORE SETTING
    # AS FINISHED
    # except Exception as e:
    #     print(e, file=sys.stderr)
