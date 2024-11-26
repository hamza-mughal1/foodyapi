from pydantic import BaseModel, validator

class OrderItem(BaseModel):
    id: int
    quantity: int
    
    @validator("quantity")
    def quantity_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Quantity must be a natural (positive) float number.")
        return value