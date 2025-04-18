from jose import jwt, ExpiredSignatureError, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, Response, Request, status
from schemas.db_schemas import users_db_schema, refresh_tokens_db_schema, access_tokens_db_schema
from utilities.utils import verify_password
from utilities.settings import setting
from sqlalchemy.future import select
import uuid
from utilities.dependencies import db_dependency
import re

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

    async def get_token(self, request: Request):
        authorization = request.cookies.get("access_token")
        token = authorization.split("Bearer ")[1]
        payload = jwt.decode(token, self.SECRET_KEY, algorithms=self.ALGORITHM)
        return payload

    async def login(self, user_credentials, db: db_dependency, response: Response):
        result = await db.execute(
            select(users_db_schema.Users).where(
                users_db_schema.Users.email == user_credentials.username
            )
        )
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=403, detail="Invalid Credentials")
        if not verify_password(user_credentials.password, user.password):
            raise HTTPException(status_code=403, detail="Invalid Credentials")

        access_token = await self.create_token(
            {"user_id": user.id, "user_name": user.username, "type": "access-token", "role": user.user_role.value}
        )

        refersh_token = await self.create_token(
            {"user_id": user.id, "user_name": user.username, "type": "refresh-token", "role": user.user_role.value}
        )
        
        try:
            db_access_token = access_tokens_db_schema(user_id=user.id, token=access_token)
            db.add(db_access_token)
            await db.flush()  # Flush to generate db_access_token.id

            # Create and add the refresh token using the generated id
            db_refresh_token = refresh_tokens_db_schema(
                user_id=user.id, 
                access_token_id=db_access_token.id, 
                token=access_token
            )
            db.add(db_refresh_token)

            await db.commit()
        except Exception as e:
            # Rollback in case of any error
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error while adding tokens to the database.")                
        
        response.set_cookie(
            key="refresh_token",
            value=f"Bearer {refersh_token}",
            httponly=True,  # Prevent JavaScript access to the cookie
            secure=True,  # Use Secure cookies (HTTPS only)
            samesite="Lax",  # Prevent CSRF attacks
            max_age=self.REFRESH_TOKEN_EXPIRE_MINUTES
            * 60,  # Set cookie expiry in seconds
            path="/refresh"         ## for a specific path
        )

        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,  # Prevent JavaScript access to the cookie
            secure=True,  # Use Secure cookies (HTTPS only)
            samesite="Lax",  # Prevent CSRF attacks
            max_age=self.ACCESS_TOKEN_EXPIRE_MINUTES
            * 60,  # Set cookie expiry in seconds
            path="/"         ## for a specific path
        )
        
        

        return {"message": "Login successful"}
    
    async def refresh(self, request: Request, db: db_dependency, response: Response):
        # Define a regex pattern to validate the basic JWT structure: header.payload.signature
        JWT_REGEX = re.compile(r"^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$")

        # ---- Access Token Validation ----
        access_token_cookie = request.cookies.get("access_token")
        if not access_token_cookie:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token missing."
            )
        if not access_token_cookie.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid access token format: missing 'Bearer' prefix."
            )
        access_token = access_token_cookie.split("Bearer ")[1]
        if not JWT_REGEX.match(access_token):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JWT access token format."
            )
        try:
            access_payload = jwt.decode(access_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Access token is not expired."
            )
        except ExpiredSignatureError:
            pass
        
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to decode access token."
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Access token validation error: {str(e)}"
            )

        # ---- Refresh Token Validation ----
        refresh_token_cookie = request.cookies.get("refresh_token")
        if not refresh_token_cookie:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token missing."
            )
        if not refresh_token_cookie.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid refresh token format: missing 'Bearer' prefix."
            )
        refresh_token = refresh_token_cookie.split("Bearer ")[1]
        if not JWT_REGEX.match(refresh_token):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JWT refresh token format."
            )
        try:
            refresh_payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired."
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to decode refresh token."
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Refresh token validation error: {str(e)}"
            )

        # ---- Database Verification ----
        # Check if the access token exists in the database.
        stmt_access = select(access_tokens_db_schema.AccessTokens).where(access_tokens_db_schema.AccessTokens.token == access_token)
        result = await db.execute(stmt_access)
        db_access_token_entry = result.scalars().first()
        if not db_access_token_entry:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token not found in the database."
            )

        # Check if the refresh token exists in the database.
        stmt_refresh = select(refresh_tokens_db_schema.RefreshTokens).where(refresh_tokens_db_schema.RefreshTokens.token == refresh_token)
        result = await db.execute(stmt_refresh)
        db_refresh_token_entry = result.scalars().first()
        if not db_refresh_token_entry:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token not found in the database."
            )

        # Optionally verify that the refresh token is associated with the access token.
        if db_refresh_token_entry.access_token_id != db_access_token_entry.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access and refresh token do not match."
            )

        