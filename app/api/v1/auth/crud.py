from sqlalchemy import select

from fastapi import Depends
from typing import Annotated

from database import SessionDep
from models import User
from .schemas import UserRegistration
from .security import get_password_hash

class UserRepository:

    def __init__(self, session: SessionDep):
        self._session = session

    async def get_user_by_email(self, email):
        query = select(User).filter_by(email=email)
        res = await self._session.execute(query)
        return res.scalars().first()

    async def create_user(self, user_: UserRegistration):
        user_.password = get_password_hash(user_.password)
        user = User(**user_.model_dump())
        self._session.add(user)
        await self._session.commit()
        return {"detail": "user added successfully"}

UserRepoDep = Annotated[UserRepository, Depends(UserRepository)]