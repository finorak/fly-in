import os
from typing import Any


def call_error() -> None:
    raise Exception()


# get_path(
#  "maps", "easy", "01_linear_path.txt"
#           )
def get_path(*args: Any) -> str:
    return os.path.join(*args)


def get_metadata(data_key: str, data: str) -> dict[str, Any]:
    if data_key == "connection":
        max_occupation = "max_link_capacity"
    else:
        max_occupation = "max_drones"
    result: dict[str, Any] = {
        max_occupation: 1,
        "zone": "normal" if data_key == "hub" else None,
        "color": None,
    }
    metadata: list[str] = data.strip("[]").split()
    if not metadata:
        return data
    for el in metadata:
        line: list[str] = el.split("=")
        key: str = line[0].strip()
        value: str | Any = line[1].strip()
        if value.isdigit():
            result[key] = int(value)
            continue
        if data_key == "connection" and (key in ("zone")):
            continue
        if data_key in ("hub", "start_hub", "end_hub") and key == "max_link_capacity":
            continue
        result[key] = value
    return result


def get_info(key: str, metadata: str) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    if key == "connection":
        data = metadata.split(" ")
        conection = data[0].strip().split("-")
        parsed["a"] = conection[0].strip()
        parsed["b"] = conection[1].strip()
        if len(data) >= 2:
            parsed["metadata"] = get_metadata(key, data[1])
    else:
        value: str | Any = metadata.split()
        parsed["hub_name"] = value[0].strip()
        parsed["x"] = int(value[1])
        parsed["y"] = int(value[2])
        if len(value) >= 4:
            parsed["metadata"] = get_metadata(key, value[3])
    return parsed


# map_info is a list of dict[str, Any]
def valid_map(map_info: list[dict[str, Any]]) -> bool:
    required_field = {"nb_drones", "start_hub", "end_hub", "hub", "connection"}
    # is_required: bool = all(required_field.issubset(dic.keys() for dic in map_info))
    return True


def parsing(file_path: str) -> list[dict[str, Any]]:
    parsed: list[dict[str, Any]] = []
    try:
        with open(file_path, encoding="utf-8", mode="r") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("#"):
                    continue
                new_dict: dict[str, Any] = {}
                curr_line: list[str] = line.strip().split(":")
                if len(curr_line) != 2:
                    continue
                key: str = curr_line[0].strip()
                value: str | Any = curr_line[1].strip()
                if value.isdigit():
                    new_dict[key] = int(value)
                else:
                    new_dict[key] = get_info(key, value)
                parsed.append(new_dict)
        if not valid_map(parsed):
            call_error()
        return parsed
    except Exception as e:
        print(e)
