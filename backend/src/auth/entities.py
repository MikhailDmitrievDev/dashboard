import re

from pydantic import BaseModel
from pydantic.v1 import validator


class UserMailAuthEntity(BaseModel):
    email: str
    password: str

    @validator('email')
    def validate_email(self, value):
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not value:
            raise ValueError('Email обязателен для заполнения')
        if not re.match(email_pattern, value):
            raise ValueError('Email некорректен')
        return value

    @validator('password')
    def validate_password(self, value):
        if not value:
            raise ValueError('Пароль обязателен для заполнения')
        if len(value) < 8:
            raise ValueError('Недостаточно символов.')
        return value


class UserSignUpEntity(UserMailAuthEntity):
    username: str

    @validator('username')
    def validate_username(self, value):
        if not value:
            raise ValueError('Имя пользователя обязательно для заполнения')
        return value


class JWTTokenResponse(BaseModel):
    """ Represents a JWT token response. """
    access: str
    refresh: str


class UserFullEntity(BaseModel):
    id: int = 4
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True
