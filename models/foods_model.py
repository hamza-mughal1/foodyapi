from sqlalchemy.ext.asyncio import AsyncSession
from schemas.db_schemas.foods_db_schema import Foods
from schemas.pydantic_schemas import foods_pydantic_schema as food_schema
from sqlalchemy.future import select
from fastapi import HTTPException, status
from utilities.utils import check_if_vendor_has_a_restaurant


class FoodModel:
    def __init__(self):
        pass

    async def create_food(self, food_data: food_schema.CreateFood, db: AsyncSession, token):
        restaurant = await check_if_vendor_has_a_restaurant(db, token)
        data = food_data.model_dump()
        data["restaurant_id"] = restaurant.id
        
        food = Foods(**data)
        db.add(food)
        await db.commit()

        return {"message": "food has been created!"}
