from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from utilities.dependencies import db_dependency
from models.authentication_model import Authentication

authentication = Authentication()

router = APIRouter(tags=["Authentication"])


@router.post("/login/")
async def login(
    db: db_dependency,
    response: Response,
    user_credentials: OAuth2PasswordRequestForm = Depends(),
):
    return await authentication.login(user_credentials, db, response)
