from fastapi import APIRouter
from utilities.dependencies import db_dependency, token_dependency
from models.restaurants_model import RestaurantsModel
from schemas.pydantic_schemas import restaurants_pydantic_schema as schema

router = APIRouter(prefix="/restaurants", tags=["retaurants"])

restaurant = RestaurantsModel()


@router.post("/")
async def create_restaurant(db: db_dependency, token: token_dependency, data: schema.CreateRestaurant):
    return await restaurant.create_restaurant(db, token, data)