from pydantic import BaseModel, validator

class CreateFood(BaseModel):
    name: str
    price: float
    
    @validator("price")
    def price_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Price must be a natural (positive) float number.")
        return value