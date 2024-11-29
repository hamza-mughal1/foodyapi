from typing import Annotated
from fastapi import Depends
from engines.sql_engine import get_db
from sqlalchemy.ext.asyncio import AsyncSession

db_dependency = Annotated[AsyncSession, Depends(get_db)]


from models.authentication_model import Authentication
authentication = Authentication()
uncheck_token = Annotated[dict, Depends(authentication.verify_token)]


from RBAC.role_based_access_control import check_access
token_dependency = Annotated[dict, Depends(check_access)]