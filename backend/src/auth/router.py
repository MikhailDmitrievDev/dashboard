from fastapi import APIRouter, HTTPException

from auth.entities import UserMailAuthEntity, UserSignUpEntity
from auth.service import AuthMailService
from repositories.postgres import PostgresRepository

router = APIRouter(
    prefix="/auth",
)


@router.post("/signin")
async def sign_in(auth_data: UserMailAuthEntity):
    auth_service = AuthMailService(PostgresRepository(None))
    try:
        tokens = await auth_service.sign_in(auth_data)
    except ValueError as err:
        raise HTTPException(status_code=401, detail=str(err))
    return tokens


@router.post("/signup")
async def sign_up(signup_data: UserSignUpEntity):
    auth_service = AuthMailService(PostgresRepository(None))
    try:
        tokens = await auth_service.sign_up(signup_data)
    except ValueError as err:
        raise HTTPException(status_code=401, detail=str(err))
    return tokens
