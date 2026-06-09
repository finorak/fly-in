from pydantic import BaseModel, model_validator

from codes.parser.map_error import MapError


class HubModel(BaseModel):
    """Hub model
    """
    name: str
    zone: str = "normal"
    index: int
    x: int
    y: int

    @model_validator(mode='after')
    def validate_model(self) -> 'HubModel':
        """Custom validator for
        the hub model.
        """
        if self.name.__contains__('-') or self.name.__contains__(' '):
            raise MapError(f"Line {self.index}: name can't have ' ' or '-'")
        return self
