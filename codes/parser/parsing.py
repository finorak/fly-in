import re
import sys
from typing import Any

from models.connection import ConnectionModel
from models.hub import HubModel
from parser.map_error import MapError


class Parser:
    """A class for parsing the map
    """
    def __init__(self, map_file: str) -> None:
        """Constructor for an instance of Parser
        Parameters:
            map_file: the location of the map
        """
        self.data: dict[str, Any] = {
                'nb_drones': 1,
                'hub': [],
                'connection': []
                }
        self.hubs: dict[str, HubModel] = {}
        self.connections: dict[str, dict[str, ConnectionModel]] = {}
        try:
            self.extract_map(map_file)
        except MapError as e:
            print(e)
            sys.exit(1)
        self.size = self.get_dimension()

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
            if not starter[0] and key == 'nb_drones':
                raise MapError(f'Line {index}: {key} already exist.')
            if key not in (
                    'start_hub', 'hub', 'end_hub',
                    'connection', 'nb_drones'
            ):
                raise MapError(f"Line {index}: Unrecognized value: {key}")
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
            if key in ('start_hub', 'hub', 'end_hub'):
                self.extract_hub(index, key, data)
            elif key == 'connection':
                self.extract_connecion(index, key, data)

    def extract_hub(self, index: int, key: str, value: str) -> None:
        """Ectracting the hub from the key, value we got
        Parameters:
            index: the current line we are in from the input file
            key: keyword of the hub.
            value: data of the hub.
        """
        splited_data: list[str] = value.split(maxsplit=3)
        if len(splited_data) not in (3, 4):
            raise MapError(f"Line {index}: Too many value to unpack")
        try:
            metadata: dict[str, Any] = {}
            name: str = splited_data[0].strip()
            x: int = int(splited_data[1].strip())
            y: int = int(splited_data[2].strip())
            if name in self.hubs:
                raise MapError(f"Line {index}: Duplicate hub.")
            if name in self.hubs:
                raise MapError(f"Line {index}: Hub already in")
            data = {
                    'name': name,
                    'x': x,
                    'y': y
                    }
            if len(splited_data) == 4:
                metadata = self.get_hub_metadata(index, splited_data[3])
            hub: HubModel = HubModel(**data, **metadata)
            self.data['hub'].append(hub)
            self.hubs[name] = hub
        except Exception as e:
            raise MapError(f"Line {index}: {e}")

    def get_hub_metadata(self, index: int, value: str) -> dict[str, str]:
        """Getting the metadata of the current hub
        Parameters:
            index: the current line of the hub.
            value: the data to where to extract the
            metadata.
        Returns:
            dict containing the metadata, else default value.
        """
        value = value.strip()
        if not (value.startswith('[') and value.endswith(']')):
            raise MapError(f"Line {index}: Metadata error.")
        pattern = r'^\[[a-zA-Z =0-9]+\]$'
        s = re.search(pattern, value)
        if not s:
            raise MapError(f"Line {index}: Metadata error.")
        # data = s.group().strip('[]')
        return {}

    def extract_connecion(self, index: int, key: str, value: str) -> None:
        """Extracting the connection from the key, value we got.
        Parameters:
            index: the current line we are in from the input file
            key: keyword of the hub.
            value: data of the hub.
        Returns:
            None
        """
        splited_value: list[str] = value.split('-', 1)
        if len(splited_value) not in (2, 3):
            raise MapError(f"Line {index}: Too many value to unpack")
        try:
            metadata: dict[str, Any] = {}
            hub_a: str = splited_value[0]
            hub_b: str = splited_value[1]
            if hub_a.__contains__('-') or hub_a.__contains__(' '):
                raise MapError(f"Line {index}: Hub name can't have ' ' or '-'")
            if hub_b.__contains__('-') or hub_b.__contains__(' '):
                raise MapError(f"Line {index}: Hub name can't have ' ' or '-'")
            if hub_a not in self.hubs or hub_b not in self.hubs:
                raise MapError(f"Line {index}: Hub name not recognized.")
            if len(splited_value) == 3:
                metadata = self.get_connection_metadata(
                        index, splited_value[2])
            data: dict[str, HubModel] = {
                    'hub_a': self.hubs[hub_a],
                    'hub_b': self.hubs[hub_b]
                    }
            connection: ConnectionModel = ConnectionModel(**data, **metadata)
            self.connections[hub_a] = {hub_b: connection}
            self.connections[hub_b] = {hub_a: connection}
        except Exception as e:
            raise MapError(f"Line {index}: {e}")

    def get_connection_metadata(
            self, index: int, value: str
            ) -> dict[str, Any]:
        """Getting the metadata of the current connection.
        Parameters:
            index: the current line of the connection inside
            the input files
            value: where to extract the metadata
        Returns:
            dict containing the metadata, else default value.
        """
        return {}

    def get_dimension(self) -> int:
        """Getting the dimension, Just iterating
        over the hubs and get the maximum between
        the x and y for all the hubs
        Returns:
            the dimension we got.
        """
        sizes: set = set()
        for hub in self.hubs:
            sizes.add(self.hubs[hub].x)
            sizes.add(self.hubs[hub].y)
        x: int = max(list(sizes))
        y: int = -min(list(sizes))
        if x > y:
            return x + 1
        return y + 1
