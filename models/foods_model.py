from sqlalchemy.ext.asyncio import AsyncSession
from schemas.db_schemas.foods_db_schema import Foods
from schemas.pydantic_schemas import foods_pydantic_schema as food_schema


class FoodModel:
    def __init__(self):
        pass

    async def create_food(self, food_data: food_schema.CreateFood, db: AsyncSession, token):
        food = Foods(**food_data.model_dump())
        db.add(food)
        await db.commit()

        return {"message": "food has been created!"}
