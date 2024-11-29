from sqlalchemy.ext.asyncio import AsyncSession
from schemas.db_schemas.restaurants_db_schema import Restaurants
from sqlalchemy.future import select
from fastapi import HTTPException


class RestaurantsModel:
    def __init__(self):
        pass

    async def create_restaurant(self, db: AsyncSession, token: dict, data):
        result = await db.execute(
            select(Restaurants).where(
                Restaurants.user_id == token["user_id"]
            )
        )
        restaurant = result.scalar_one_or_none()
        
        if restaurant is not None:
            raise HTTPException(status_code=409, detail="Cannot create multiple restaurants.")
        
        restaurant = Restaurants(user_id=token["user_id"], name=data.name)
        db.add(restaurant)
        await db.commit()
        
        return {"message":"Restaurant has been created!"}

