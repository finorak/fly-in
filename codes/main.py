import sys

from utils.parsing import get_path, parsing

try:
    from engine.app import App
except ImportError as e:
    print(e)
    sys.exit(1)


def main() -> None:
    if len(sys.argv) < 2:
        print("Argument error")
        sys.exit(1)
    try:
        path = sys.argv[1].split("/")
        config = parsing(get_path(*path))
        app = App(config)
        app.run()
        sys.exit(0)
    except ValueError as e:
        print(e)
        sys.exit(1)
    except KeyError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
