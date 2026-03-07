from pydantic import BaseModel, field_validator, ConfigDict
from typing import TypeVar

T = TypeVar('T')

class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    username: str

class UserAuthentication(UserBase):
    password_hash: str

class UserRegistration(UserBase):
    password_hash: str

    @field_validator('password_hash')
    @classmethod
    def validate_password(cls, password_: str):
        if password_.upper() == password_:
            raise ValueError('Треубется хотя бы одна буква в нижнем регистре')
        if password_.lower() == password_:
            raise ValueError('Треубется хотя бы одна буква в верхнем регистре')
        if not any(symbol.isdigit() for symbol in password_):
            raise ValueError('Треубется хотя бы одна цифра')
        return password_


class TokenBase(BaseModel):
    access_token: str
    token_type: str


class BaseResponse[T](BaseModel):
    status: bool = True
    detail: T | None = None
