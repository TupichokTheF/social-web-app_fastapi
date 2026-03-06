from pydantic import BaseModel, field_validator, ConfigDict

class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str

class UserAuthentication(UserBase):
    password: str

class UserRegistration(UserBase):
    password: str

    @field_validator('password')
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