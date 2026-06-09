from pydantic import BaseModel, model_validator


class ConnectionModel(BaseModel):
    """Connection model
    """
    x: int
    y: int

    @model_validator(mode='after')
    def validate_model(self) -> 'ConnectionModel':
        """A custom validator for the
        connection
        """
        return self
