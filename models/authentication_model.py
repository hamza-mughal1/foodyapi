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
