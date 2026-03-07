from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer

from typing import Annotated

from api.v1.routes.auth.crud import UserRepoDep
from api.v1.routes.auth.schemas import UserBase
from api.v1.routes.auth.service import AuthServiceDepends
from core.settings import settings

import jwt
from jwt.exceptions import InvalidTokenError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/signin")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], user_rep: UserRepoDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM_OF_CIFER])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await user_rep.get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user

async def check_authorization(auth_service: AuthServiceDepends,
                              current_user: Annotated[UserBase, Depends(get_current_user)],
                              refresh_token: Annotated[str, Cookie()]
                              ):
    email = await auth_service.get_email_by_refresh_token(refresh_token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user

AuthorizationDep = Annotated[UserBase, Depends(check_authorization)]