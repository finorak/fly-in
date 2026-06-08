from pydantic import BaseModel, model_validator


class ConnectionModel(BaseModel):
    x: int
    y: int

    @model_validator(mode='after')
    def validate_model(self) -> 'ConnectionModel':
        return self
