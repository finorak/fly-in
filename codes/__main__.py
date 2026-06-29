import sys

import pygame
from algorithm.new_algo import Algo
from parser.parsing import Parser
from src.app import App
from utils.helper import get_args


def main() -> None:
    """Entry point of the program
    """
    args = get_args()
    parser = Parser(args.input)
    app = App(parser, args.visual)
    # this will be only activated
    # if visualizer was added as
    # a parrameters
    app.init_gui()
    app._init()
    turn = Algo(app.data.drones, app.data.cells, app.data.dict_connections)
    turn.solve()
    # this function is same as init_gui
    app.run()


if __name__ == "__main__":
    try:
        main()
    except pygame.error as e:
        print(e, file=sys.stderr)
