from pydantic import BaseModel


class HubModel(BaseModel):
    name: str
    x: int
    y: int

    @model_validator(mode='after')
    def validate_model(self) -> 'HubModel':
        return self
