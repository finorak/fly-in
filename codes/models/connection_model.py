from models.hub_model import HubModel
from pydantic import BaseModel, model_validator


class ConnectionModel(BaseModel):
    """Connection model
    """
    hub_a: HubModel
    hub_b: HubModel

    @model_validator(mode='after')
    def validate_model(self) -> 'ConnectionModel':
        """A custom validator for the
        connection
        """
        if self.hub_a.name == self.hub_b.name:
            raise ValueError("Can't connect two equal hub")
        return self

    def __str__(self) -> str:
        """Visual representaion of this class
        """
        return f"{self.hub_a} -> {self.hub_b}"
