from sqlalchemy.ext.asyncio import AsyncSession
from schemas.db_schemas.users_db_schema import Users
from schemas.pydantic_schemas.users_pydantic_schema import CreateUser
from utilities.utils import create_hashed_password


class UsersModel:
    def __init__(self):
        pass

    async def create_user(self, user_data: CreateUser, db: AsyncSession):
        data = user_data.model_dump()
        data.update(password=create_hashed_password(data["password"]))
        user = Users(**data)
        db.add(user)
        await db.commit()

        return {"message": "user has been created!"}
