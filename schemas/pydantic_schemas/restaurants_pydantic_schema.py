from pydantic import BaseModel

class CreateRestaurant(BaseModel):
    name: str
