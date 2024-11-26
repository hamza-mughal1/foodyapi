import re
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Request, Response
from schemas.db_schemas import users_db_schema
from utilities.utils import verify_password
from utilities.settings import setting
from sqlalchemy.future import select
import uuid
from fastapi import HTTPException, status
from utilities.dependencies import db_dependency


class Authentication:
    def __init__(
        self,
        secret_key=setting.secret,
        algorithm=setting.algorithm,
        access_token_expire_minutes=setting.access_token_expire_minutes,
        refresh_token_expire_minutes=setting.refresh_token_expire_minutes,
    ):
        self.SECRET_KEY = secret_key
        self.ALGORITHM = algorithm
        self.ACCESS_TOKEN_EXPIRE_MINUTES = access_token_expire_minutes
        self.REFRESH_TOKEN_EXPIRE_MINUTES = refresh_token_expire_minutes

    @staticmethod
    async def get_token(request: Request):
        authorization = request.cookies.get("access_token")
        if authorization is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing token",
            )
        # Check if the Authorization header starts with "Bearer "
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing token",
            )

        # Extract the token part
        token = authorization.split("Bearer ")[1]

        # Define a regex pattern for a valid token
        token_pattern = r"^[A-Za-z0-9\-_]+\.([A-Za-z0-9\-_]+)?\.([A-Za-z0-9\-_]+)?$"  # Basic JWT structure

        # Check if the token matches the regex
        if not re.match(token_pattern, token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Malformed or invalid token",
            )

        return token

    async def create_token(self, data: dict, refresh=False):
        to_encode = data.copy()
        if refresh:
            expiration = datetime.now() + timedelta(
                minutes=self.REFRESH_TOKEN_EXPIRE_MINUTES
            )
        else:
            expiration = datetime.now() + timedelta(
                minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": round(expiration.timestamp())})
        to_encode.update({"uuid": str(uuid.uuid4())})

        ecoded_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

        return ecoded_token

    async def verify_token(self, db: db_dependency, token: str = Depends(get_token)):
        token = await token
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=self.ALGORITHM)
            user_id = payload.get("user_id")
            user_name = payload.get("user_name")

            if (user_id is None) or (user_name is None):
                raise HTTPException(
                    status_code=403,
                    detail="token is invalid",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            result = await db.execute(
                select(users_db_schema.Users).where(users_db_schema.Users.id == user_id)
            )

            if (user := result.scalar_one_or_none()) is None:
                raise HTTPException(
                    status_code=403,
                    detail="Invalid token. (User not found)",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            payload.update({"user_name": user.username, "token": token})

        except JWTError:
            raise HTTPException(
                status_code=403,
                detail="token is invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload

