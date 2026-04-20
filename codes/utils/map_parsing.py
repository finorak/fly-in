import os
from typing import Any


# get_path(
#  "maps", "easy", "01_linear_path.txt"
#           )
def get_path(*args: Any) -> Any:
    return os.path.join(*args)


def get_metadata(data_key: str,
                 data: str | None = None) -> dict[str | None, Any]:
    if data_key.__contains__("hub"):
        capacity = "max_drones"
    else:
        capacity = "max_link_capacity"
    if data_key in ("end_hub", "start_hub"):
        zone_value = "priority"
        zone = "zone"
    elif data_key == 'hub':
        zone_value = "normal"
        zone = "zone"
    else:
        zone_value = None
        zone = None
    result: dict[str | None, Any] = {
        "color": None,
        capacity: 1,
        zone: zone_value,
    }
    if data is None:
        return result
    metadata: list[str] = data.strip("[]").split()
    for val in metadata:
        dt = val.strip().split("=")
        key: str = dt[0].strip()
        value: str | Any = dt[1].strip()
        if value.isdigit():
            value = int(value)
        result.update({key: value})
    return result


def get_hub_data(key: str, data: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    line: list[str] = data.split(maxsplit=3)
    result["name"] = line[0].strip()
    result["x"] = int(line[1].strip())
    result["y"] = int(line[2].strip())
    result["metadata"] = get_metadata(
            "hub", line[3] if len(line) == 4 else None)
    return result


def get_connection(data: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    val: list[str] = data.split(maxsplit=2)
    points: list[str] = val[0].strip().split("-")
    result["a"] = points[0]
    result["b"] = points[1]
    result["metadata"] = get_metadata(
            "con", val[1] if len(val) == 2 else None)
    return result


def parsing(file_path: str) -> dict[str, Any] | None:
    data: dict[str, Any] = {}
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                new_line: str = line.strip()
                if new_line.startswith("#"):
                    continue
                curr_line: list[str] = new_line.split(":", maxsplit=2)
                if len(curr_line) != 2:
                    continue
                key: str = curr_line[0].strip()
                value: Any = curr_line[1].strip()
                if key == "nb_drones":
                    if key in data:
                        raise Exception("Map error!!")
                    data[key] = int(value)
                elif key == "start_hub":
                    if key in data:
                        raise Exception("Map Error!!")
                    data[key] = get_hub_data(key, value)
                elif key == "end_hub":
                    if key in data:
                        raise Exception("Map Error!!")
                    data[key] = get_hub_data(key, value)
                elif key == "hub":
                    if "hub" not in data:
                        data["hub"] = []
                    data["hub"].append(get_hub_data(key, value))
                elif key == "connection":
                    if key not in data:
                        data[key] = []
                    data[key].append(get_connection(value))
        if (
                "nb_drones" not in data
                or "hub" not in data
                or "connection" not in data
        ):
            raise Exception("Map error")
        return data
    except Exception as e:
        print(data)
        print(e)
        return None
