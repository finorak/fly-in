import re
from typing import Any

from models.connection_model import ConnectionModel
from models.hub_model import HubModel
from settings import PATTERN, ZONES
from utils.errors import MapError
from utils.helper import (
    duplicate_connection,
    duplicate_position,
    get_dimension,
    is_numeric,
)


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
        self.key_found: set[str] = set()
        self.conns: list[ConnectionModel] = []
        # EXTRACTING THE MAP FILES
        self.extract_map(map_file)
        self.size: tuple[int, int, int, int] = get_dimension(self.hubs)

    def extract_map(self, map_file: str) -> None:
        """Extracting input file
        Parameters:
            map_file: the location of the map
        """
        with open(map_file, mode='r', encoding='utf-8') as file:
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
            if (not starter[0] and key == 'nb_drones') \
                    or (not starter[1] and key == 'start_hub') \
                    or (not starter[2] and key == 'end_hub'):
                raise MapError(f"Line {index}: Start hub already exist.")
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
                if key == 'start_hub':
                    starter[1] = False
            if starter[2]:
                if key == 'end_hub':
                    starter[2] = False
            if key in ('start_hub', 'hub', 'end_hub'):
                self.extract_hub(index, key, data)
            elif key == 'connection':
                self.extract_connecion(index, key, data)
            self.key_found.add(key)

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
            metadata: dict[Any, Any] = {}
            name: str = splited_data[0].strip()
            x: str = splited_data[1].strip()
            y: str = splited_data[2].strip()
            if not is_numeric(x) or not is_numeric(y):
                raise MapError(f"Line {index}: position must be valid integer")
            if name in self.hubs:
                raise MapError(f"Line {index}: Duplicate hub.")
            if name in self.hubs:
                raise MapError(f"Line {index}: Hub already in")
            data: dict[Any, Any] = {
                    'name': name,
                    'x': x,
                    'y': y
                    }
            if len(splited_data) == 4:
                metadata = self.get_hub_metadata(index, splited_data[3])
            hub: HubModel = HubModel(**data, **metadata)
            if duplicate_position(self.data['hub'], hub):
                raise MapError("Position can't be duplicate")
            self.data['hub'].append(hub)
            self.hubs[name] = hub
            if key == "start_hub":
                self.start = name
            elif key == "end_hub":
                self.end = name
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
        string = re.search(PATTERN, value)
        if not string:
            raise MapError(f"Line {index}: Metadata error.")
        splitted_string: list[str] = string.group().strip('[]').split()
        data: dict[str, Any] = {}
        for el in splitted_string:
            splited = el.split('=')
            if len(splited) != 2:
                raise MapError(f"Line {index}: Metadata Error")
            key: str = splited[0].strip()
            key_value: str = splited[1].strip()
            if key == 'zone':
                if key_value not in ZONES:
                    raise MapError(f'Line {index}: Zone not recognized.')
                data['zone'] = key_value
            elif key == 'max_drones':
                if not key_value.isdigit():
                    raise MapError(f"Line {index}: Value must be integer.")
                data[key] = int(key_value)
            elif key == 'color':
                data[key] = key_value
            else:
                raise MapError(f"Line {index}: Value not recognized.")
        return data

    def extract_connecion(self, index: int, key: str, value: str) -> None:
        """Extracting the connection from the key, value we got.
        Parameters:
            index: the current line we are in from the input file
            key: keyword of the hub.
            value: data of the hub.
        Returns:
            None
        """
        if 'start_hub' not in self.key_found or \
                'end_hub' not in self.key_found:
            raise MapError(f"Line {index}: 'start_hub' or 'end_hub' not found")
        splited_value: list[str] = value.split(maxsplit=2)
        if len(splited_value) not in (1, 2):
            raise MapError(f"Line {index}: Too many value to unpack")
        connections: list[str] = splited_value[0].split('-', maxsplit=1)
        try:
            metadata: dict[str, Any] = {}
            hub_a: str = connections[0]
            hub_b: str = connections[1]
            if hub_a.__contains__('-') or hub_a.__contains__(' '):
                raise MapError(f"Line {index}: Hub name can't have ' ' or '-'")
            if hub_b.__contains__('-') or hub_b.__contains__(' '):
                raise MapError(f"Line {index}: Hub name can't have ' ' or '-'")
            if hub_a not in self.hubs or hub_b not in self.hubs:
                raise MapError(f"Line {index}: Hub name not recognized.")
            if len(splited_value) == 2:
                metadata = self.get_connection_metadata(
                        index, splited_value[1])
            data: dict[str, Any] = {
                    'hub_a': self.hubs[hub_a],
                    'hub_b': self.hubs[hub_b]
                    }
            connection: ConnectionModel = ConnectionModel(
                    **data, **metadata, connecton_name=connections
                    )
            self.connections[hub_a] = {hub_b: connection}
            if duplicate_connection(self.conns, connection):
                raise MapError("Duplicate connection")
            self.conns.append(connection)
        except Exception as e:
            raise MapError(f"Line {index}: {e}")

    def get_connection_metadata(
            self, index: int, value: str
            ) -> dict[str, int]:
        """Getting the metadata of the current connection.
        Parameters:
            index: the current line of the connection inside
            the input files
            value: where to extract the metadata
        Returns:
            dict containing the metadata, else default value.
        """
        string_match = re.search(PATTERN, value)
        if not string_match:
            raise MapError(f"Line {index}: Metadata error.")
        string = string_match.group().strip('[]')
        splited_string = string.split('=')
        if len(splited_string) != 2:
            raise MapError(f"Line {index}: Metadata error.")
        if splited_string[0] != 'max_link_capacity':
            raise MapError(f"Line {index}: Unrecognized metadata value.")
        if not splited_string[1].isdigit():
            raise MapError(f"Line {index}: Value must be positive integer")
        return {splited_string[0]: int(splited_string[1])}
