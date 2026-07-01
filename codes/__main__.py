import sys
from algorithm.custom_bfs import CustomBFS
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
    app.init()
    turn = CustomBFS(
        app.data.drones,
        app.data.cells,
        app.data.dict_connections
    )
    turn.solve()
    # this function is same as init_gui
    if args.visual:
        app.run(turn.drones_cpy)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e, file=sys.stderr)
