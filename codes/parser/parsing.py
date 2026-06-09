import sys
from typing import Any

from parser.map_error import MapError


class Parser:
    """A class for parsing the map
    """
    def __init__(self, map_file: str) -> None:
        """Constructor for an instance of Parser
        Parameters:
            map_file: the location of the map
        """
        self.data: dict[str, Any] = {}
        try:
            self.extract_map(map_file)
        except MapError as e:
            print(e)
            sys.exit(1)

    def extract_map(self, map_file: str) -> None:
        """Extracting input file
        Parameters:
            map_file: the location of the map
        """
        with open(map_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        starter: list[bool] = [True, True, True]
        for index, line in enumerate(lines, start=1):
            if not line.strip() or line.strip().startswith("#"):
                continue
            line = line.strip()
            curr_line: list[str] = line.split(':')
            if len(curr_line) != 2:
                raise MapError(f"Line {index}: Too many value to unpack.")
            key: str = curr_line[0].strip()
            data: Any = curr_line[1].strip()
            if key not in (
                    'start_hub', 'hub', 'end_hub',
                    'connection', 'nb_drones'
            ):
                raise MapError(f"Line {index}: Unrecognized value: {key}")
            if (
                    (not starter[0] and key == 'nb_drones')
                    or (not starter[1] and key == 'start_hub')
                    or (not starter[2] and key == 'end_hub')
            ):
                raise MapError(f"Line {index}: '{key}' already exist")
            if starter[0]:
                if key != 'nb_drones':
                    raise MapError(f"Line {index}: must be 'nb_coders'.")
                try:
                    data = int(curr_line[1].strip())
                    if data < 0:
                        raise MapError(
                                f"Line {index}: value must "
                                "be positiv integer.")
                except Exception:
                    raise MapError(
                            f"Line {index}: value must "
                            "be positiv integer.")
                self.data['nb_drones'] = data
                starter[0] = False
            if starter[1]:
                if key != 'start_hub':
                    continue
                self.extract_hub(index, key, data)
                starter[1] = False
            if starter[2]:
                if key != 'end_hub':
                    continue
                self.extract_hub(index, key, data)
                starter[2] = False
            if key == 'hub':
                self.extract_hub(index, key, data)
            if key == 'connection':
                self.extract_connecion(index, key, data)

    def extract_hub(self, index: int, key: str, data: str) -> None:
        """Ectracting the hub from the key, value we got
        Parameters:
            index: the current line we are in from the input file
            key: keyword of the hub.
            value: data of the hub.
        Returns:
            None
        """

    def extract_connecion(self, index: int, key: str, data: str) -> None:
        """Extracting the connection from the key, value we got.
        Parameters:
            index: the current line we are in from the input file
            key: keyword of the hub.
            value: data of the hub.
        Returns:
            None
        """
        return

    def get_dimension(self) -> tuple[int, int]:
        """Getting the dimension of the
        """
        return 0, 0
