from fastapi import Depends
from typing import Annotated

from datetime import timedelta, datetime, timezone
import jwt

from core.settings import settings
from .crud import UserRepoDep
from .security import verify_password
from .schemas import UserAuthentication, UserRegistration
from database import RedisDep

class AuthService:
    _ALGORITHM: str = settings.ALGORITHM_OF_CIFER
    _JWT_SECRET_KEY: str = settings.JWT_SECRET_KEY

    def __init__(self, repo: UserRepoDep, redis_: RedisDep):
        self._repository = repo
        self._redis = redis_

    async def authenticate_user(self, user_: UserAuthentication):
        user = await self._repository.get_user_by_email(user_.email)
        if not user:
            return False
        if not verify_password(user_.password, user.password):
            return False
        return user

    async def generate_refresh_token(self, data: dict):
        encoded_jwt = await self.generate_token(data, settings.REFRESH_TOKEN_EXPIRES)
        self._redis.set(name=f"refresh_token:{encoded_jwt}", value=f"email:{data['sub']}", ex=86400)
        return encoded_jwt

    async def generate_token(self, data: dict, expires_delta: timedelta | None = settings.ACCESS_TOKEN_EXPIRES):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self._JWT_SECRET_KEY, algorithm=self._ALGORITHM)
        return encoded_jwt

    async def create_user(self, user_: UserRegistration):
        try:
            return await self._repository.create_user(user_)
        except Exception as e:
            raise e

    async def logout(self, refresh_token: str):
        self._redis.delete(f"refresh_token:{refresh_token}")

AuthServiceDepends = Annotated[AuthService, Depends(AuthService)]