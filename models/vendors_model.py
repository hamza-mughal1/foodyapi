from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.db_schemas import db_enums
from schemas.db_schemas import users_db_schema


class VendorsModel:
    def __init__(self):
        pass

    async def upgrade_to_vendor(self, db: AsyncSession, token: dict):
        result = await db.execute(
            select(users_db_schema.Users).where(
                users_db_schema.Users.id == token["user_id"]
            )
        )
        user = result.scalar_one_or_none()
        user.user_role = db_enums.UserRole.vendor.value
        
        await db.commit()
        
        return {"message": "user has been promoted to vendor"}