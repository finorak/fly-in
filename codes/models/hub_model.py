from pydantic import BaseModel, model_validator


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
            raise ValueError("Hub name can't contain ' ' or '-'")
        return self

    def __str__(self) -> str:
        """Visual representaion of this class
        """
        return f"{self.name}, pos=({self.x}, {self.y})"
