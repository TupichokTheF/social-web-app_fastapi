from fastapi import APIRouter, HTTPException, status, Response, Cookie

from .service import AuthServiceDepends
from .schemas import UserAuthentication, TokenBase, UserRegistration, BaseResponse
from .exceptions import WrongEmail

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication operations"],
)

@auth_router.post("/signin", response_model=TokenBase)
async def login_user(service: AuthServiceDepends, user_: UserAuthentication, response: Response):
    user = await service.authenticate_user(user_)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await service.generate_token({"sub": user_.email})
    refresh_token = await service.generate_refresh_token({"sub": user_.email})
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        max_age=24 * 60 * 60
    )
    return TokenBase(access_token=access_token, token_type="bearer")


@auth_router.post("/signup", response_model=BaseResponse)
async def signup_user(service: AuthServiceDepends, user_: UserRegistration):
    try:
        await service.create_user(user_)
        return BaseResponse(detail="User was created successfully")
    except WrongEmail as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@auth_router.post("/logout", response_model=BaseResponse)
async def logout_user(service: AuthServiceDepends, refresh_token = Cookie()):
    await service.logout(refresh_token)
    return BaseResponse(detail="User was logged out")

