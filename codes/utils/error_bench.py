import sys
from typing import Any


def show_log(msg: Any) -> None:
    print(msg, file=sys.stderr)
