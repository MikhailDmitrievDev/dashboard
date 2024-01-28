from datetime import timedelta, datetime
from typing import Union

from jose import jwt
from pydantic import BaseModel

import settings
from .entities import JWTTokenResponse, UserMailAuthEntity, UserFullEntity, UserSignUpEntity
from .interfaces import IAuthService


class UserService(object):
    users = [
        {
            "id": 1,
            "username": "admin",
            "password": "123",
            "email": "admin@test.com"
        },
        {
            "id": 2,
            "username": "moder",
            "password": "123",
            "email": "moder@test.com"
        }
    ]

    def __init__(self, repository):
        self.repository = repository

    @classmethod
    async def get_user(cls, auth_data: BaseModel) -> Union[UserFullEntity, None]:
        """
        Get user from repository and return user entity.
        :return: User entity
        """
        for user in cls.users:
            if user.get("email") == auth_data.email:
                return UserFullEntity.model_validate(user)
        return None

    async def create_user(self, signup_data: UserSignUpEntity) -> UserFullEntity:
        UserService.users.append(signup_data.model_dump())
        new_user = await UserService.get_user(signup_data)
        return UserFullEntity.model_validate(new_user.model_dump())


class AuthMailService(IAuthService):

    def __init__(self, repository):
        self.user_service = UserService(repository)

    @classmethod
    def verify_password(cls, current_password: str, user_password: str):
        """
        Verify password.

        :param current_password: str received from the client
        :param user_password: str received from the repository
        :return: bool
        """
        if current_password == user_password:
            return True
        return False

    async def sign_in(self, auth_data: UserMailAuthEntity) -> JWTTokenResponse:
        user = await self.user_service.get_user(auth_data)
        if not self.verify_password(auth_data.password, user.password):
            raise ValueError("Неверный пароль")
        return JWTService.token_response(user.id)

    async def sign_up(self, signup_data: UserSignUpEntity):
        user = await self.user_service.get_user(signup_data)
        if not user:
            new_user = await self.user_service.create_user(signup_data)
            return JWTService.token_response(new_user.id)
        raise ValueError("Пользователь с таким email уже существует")


class JWTService(object):

    @classmethod
    def encode(cls, type_token: str, user_id, exp: int) -> str:
        """
        Encode token

        :param type_token: str type token
        :param user_id: int id user
        :param exp: time in minutes
        :return: str: token
        """
        exp = datetime.now() + timedelta(seconds=exp)
        scope = {
            "type": type_token,
            "user_id": user_id,
            "exp": exp
        }
        token = jwt.encode(scope, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return token

    @classmethod
    def decode(cls, token: str) -> dict:
        """
        Decode token

        :param token: str token
        :return: dict scope data
        :raise: ValueError if token expired
        """

        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise ValueError("Время защиты токена истекло.")

    @classmethod
    def token_response(cls, user_id: int) -> JWTTokenResponse:
        """
        Create tokens for client.

        :param user_id: current user id
        :return: JWTTokenResponse entity with tokens
        """

        return JWTTokenResponse(
            access=cls.encode("access", user_id, settings.ACCESS_TOKEN_EXPIRE_SECONDS),
            refresh=cls.encode("refresh", user_id, settings.REFRESH_TOKEN_EXPIRE_SECONDS),
        )
