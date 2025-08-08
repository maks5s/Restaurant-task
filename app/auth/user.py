from fastapi import HTTPException, status, Depends, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.models import User, db_helper, Employee, Restaurant
from app.core.schemas.auth import TokenInfo, LoginSchema, LogoutMessage
from app.crud import user as crud_user
from app.crud import employee as crud_employee
from app.crud import restaurant as crud_restaurant
from app.auth import utils as auth_utils

http_bearer = HTTPBearer()


async def validate_auth_user(
    login_data: LoginSchema,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    unauthed_exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    user = await crud_user.get_user_by_username(session, login_data.username)
    if not user:
        raise unauthed_exc

    if not auth_utils.validate_password(
        password=login_data.password,
        hashed_password=user.hashed_password,
    ):
        raise unauthed_exc

    return user


async def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
):
    token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid access token'
        )

    return payload


async def get_refresh_token_payload(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing in cookies",
        )
    try:
        payload = auth_utils.decode_jwt(refresh_token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    return payload


async def validate_token_type(
    payload: dict,
    token_type: str,
):
    current_token_type = payload.get(settings.auth_jwt.token_type_field)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid token type {current_token_type!r} expected {token_type!r}",
    )


async def get_user_by_token_sub(payload: dict, session: AsyncSession):
    user_id = int(payload.get("sub"))

    user = await crud_user.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid (user not found)",
        )

    return user


async def get_current_auth_user(
    session: AsyncSession = Depends(db_helper.session_getter),
    payload: dict = Depends(get_current_token_payload)
):
    await validate_token_type(payload, settings.auth_jwt.access_token_type)
    return await get_user_by_token_sub(payload, session)


async def get_current_auth_user_for_refresh(
    session: AsyncSession = Depends(db_helper.session_getter),
    payload: dict = Depends(get_refresh_token_payload)
):
    await validate_token_type(payload, settings.auth_jwt.refresh_token_type)
    return await get_user_by_token_sub(payload, session)


async def get_employee_for_restaurant(
    restaurant_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(get_current_auth_user),
    restaurant: Restaurant = Depends(crud_restaurant.check_restaurant_exists)
):
    employee = await crud_employee.get_employee_by_user_and_restaurant(
        session=session,
        user_id=user.id,
        restaurant_id=restaurant_id
    )
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not an employee of this restaurant"
        )
    return await crud_employee.get_employee_with_user(session, employee.id)


async def get_admin_employee_for_restaurant(
    restaurant_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    employee: Employee = Depends(get_employee_for_restaurant),
):
    if not employee.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not an admin of this restaurant"
        )
    return employee


async def get_tokens_via_login(
    user: User,
    response: Response
):
    access_token = auth_utils.create_access_token(user)
    refresh_token = auth_utils.create_refresh_token(user)

    response.set_cookie(
        key=settings.auth_jwt.refresh_token,
        value=refresh_token,
        httponly=True,
        samesite="strict",
        secure=True,
        max_age=settings.auth_jwt.refresh_token_expire_minutes * 60,
        path="/"
    )

    return TokenInfo(
        access_token=access_token,
        token_type="Bearer",
    )


async def handle_logout(
    response: Response
):
    response.delete_cookie("refresh_token")
    return LogoutMessage(
        message="Logged out"
    )


async def get_access_token_via_refresh(
    user: User,
):
    access_token = auth_utils.create_access_token(user)

    return TokenInfo(
        access_token=access_token,
        token_type="Bearer",
    )
