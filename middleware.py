import json
from pathlib import Path
from fastapi import HTTPException, Request, status
import re
from engines.sql_engine import AsyncSessionLocal
from jose import jwt, JWTError
from sqlalchemy.future import select
from schemas.db_schemas import users_db_schema
from utilities.settings import setting
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

FILE_PATH = "access_config.json"


class AuthenticationMiddleware(BaseHTTPMiddleware):
    @staticmethod
    def get_config_file_path(filename: str = "access_config.json") -> str:
        """
        Returns the absolute path to the configuration file in the same directory as the script.
        """
        # Get the directory of the current script
        script_dir = Path(__file__).resolve().parent
        # Construct the full path to the config file
        config_file_path = script_dir / filename
        return str(config_file_path)

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

    @staticmethod
    async def verify_token(db, token, SECRET_KEY, ALGORITHM):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
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

            if (result.scalar_one_or_none()) is None:
                raise HTTPException(
                    status_code=403,
                    detail="Invalid token. (User not found)",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        except JWTError:
            raise HTTPException(
                status_code=403,
                detail="token is invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload

    @staticmethod
    async def check_access(request: Request, token: dict):
        CONFIG_FILE = AuthenticationMiddleware.get_config_file_path(filename=FILE_PATH)
        endpoint_path = request.url.path
        user_role = token["role"]

        try:
            with open(CONFIG_FILE, "r") as f:
                roles_config = json.load(f)
        except FileNotFoundError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        routes = roles_config.get("routes")
        allowed_roles = routes.get(endpoint_path)

        if allowed_roles is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden: insufficient permissions",
            )
        elif (user_role not in allowed_roles) and (not "all" in allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden: insufficient permissions",
            )

        return token

    async def dispatch(self, request: Request, call_next):
        config_file_path = AuthenticationMiddleware.get_config_file_path(
            filename=FILE_PATH
        )

        with open(config_file_path, "r") as f:
            config_data = json.load(f)

        # Check if the request path is in the excluded endpoints
        excluded_endpoints = config_data.get("excluded_endpoints", [])
        if (request.url.path in excluded_endpoints) or (
            request.url.path + "/" in excluded_endpoints
        ):
            return await call_next(request)
        secret_key = setting.secret
        algorithm = setting.algorithm
        try:
            token = await AuthenticationMiddleware.get_token(request)
            async with AsyncSessionLocal() as db:
                payload = await AuthenticationMiddleware.verify_token(
                    db, token, secret_key, algorithm
                )
            await AuthenticationMiddleware.check_access(request, payload)
            return await call_next(request)
        except Exception as e:
            try:
                return JSONResponse(status_code=e.status_code, content=e.detail)
            except:
                raise e
