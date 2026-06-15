from typing import Any

from pydantic import BaseModel, model_validator

from utils.errors import MapError


class HubModel(BaseModel):
    """Hub model
    """
    name: str
    x: int
    y: int
    zone: str = "normal"
    max_drones: int = 1
    color: str = ""

    @model_validator(mode='after')
    def validate_model(self) -> 'HubModel':
        """Custom validator for
        the hub model.
        """
        if self.name.__contains__('-') or self.name.__contains__(' '):
            raise MapError("Hub name can't contain ' ' or '-'")
        return self

    def keys(self) -> list[str]:
        """To avoid generating a key for each
        attributes in the process of creating
        the class, we just give it the keys.
        In other word, we unpack it.
        Returns:
            a list of keys we want to use
        """
        return ['x', 'y', 'name', 'zone', 'max_drones', 'color']

    def __getitem__(self, key: str) -> Any:
        """Returning the value associated with each key.
        Parameters:
            key: the key we want to use.
        Returns:
             A dictionary that contain the
             key an the value of each key.
        """
        if key in self.keys():
            return getattr(self, key)
        raise KeyError(key)

    def __str__(self) -> str:
        """Visual representaion of this class
        """
        return f"{self.name}, pos=({self.x}, {self.y})"
