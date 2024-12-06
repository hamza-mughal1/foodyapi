from fastapi import APIRouter
from schemas.pydantic_schemas import foods_pydantic_schema as food_schema
from models.foods_model import FoodModel
from utilities.dependencies import db_dependency, token_dependency

# router object to create routes 
router = APIRouter(prefix="/foods", tags=["foods"])

# food model class object to call it's functions
food = FoodModel()


@router.post("/")
async def create_food(food_data: food_schema.CreateFood, db: db_dependency, token: token_dependency):
    return await food.create_food(food_data, db, token)
