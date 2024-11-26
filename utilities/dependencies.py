from typing import Annotated
from fastapi import Depends
from engines.sql_engine import get_db
from sqlalchemy.ext.asyncio import AsyncSession

db_dependency = Annotated[AsyncSession, Depends(get_db)]

from models.authentication_model import Authentication
authentication = Authentication()

token_dependency = Annotated[dict, Depends(authentication.verify_token)]