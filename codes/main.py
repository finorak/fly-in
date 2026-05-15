import sys

try:
    from engine.app import App
except ImportError as e:
    print(e)
    sys.exit(1)


def main() -> None:
    if len(sys.argv) < 2:
        print("Argument error")
        sys.exit(1)
    path = sys.argv[1].split("/")
    app = App(*path)
    app.run()


if __name__ == "__main__":
    main()
