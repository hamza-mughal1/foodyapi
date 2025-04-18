from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.future import select
from schemas.db_schemas.restaurants_db_schema import Restaurants

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_hashed_password(passowrd):
    return pwd_context.hash(passowrd)


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

async def check_if_vendor_has_a_restaurant(db, token):
    result = await db.execute(select(Restaurants).where(Restaurants.user_id==token["user_id"]))
    restaurant = result.scalar_one_or_none()
    if restaurant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Restaurant Not Found (First Create A Restaurant)")
    
    return restaurant