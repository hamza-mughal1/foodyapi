from sqlalchemy.ext.asyncio import AsyncSession
from schemas.db_schemas.foods_db_schema import Foods
from schemas.db_schemas.restaurants_db_schema import Restaurants
from schemas.pydantic_schemas import foods_pydantic_schema as food_schema
from sqlalchemy.future import select
from fastapi import HTTPException, status


class FoodModel:
    def __init__(self):
        pass

    async def create_food(self, food_data: food_schema.CreateFood, db: AsyncSession, token):
        result = await db.execute(select(Restaurants).where(Restaurants.user_id==token["user_id"]))
        restaurant = result.scalar_one_or_none()
        if restaurant is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Restaurant Not Found (First Create A Restaurant)")
        
        data = food_data.model_dump()
        data["restaurant_id"] = restaurant.id
        
        food = Foods(**data)
        db.add(food)
        await db.commit()

        return {"message": "food has been created!"}
