from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User, db_helper
from app.core.schemas.auth import LoginSchema, TokenInfo, RegisterSchema, LogoutMessage
from app.auth import user as auth_user
from app.core.schemas.user import UserReadSchema
from app.crud import user as crud_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserReadSchema)
async def register(
    register_data: RegisterSchema,
    session: AsyncSession = Depends(db_helper.session_getter)
):
    return await crud_user.create_user(register_data, session)


@router.post("/login", response_model=TokenInfo)
async def auth_user_issue_jwt(
    login_data: LoginSchema,
    response: Response,
    user: User = Depends(auth_user.validate_auth_user),
):
    return await auth_user.get_tokens_via_login(user, response)


@router.post("/refresh", response_model=TokenInfo)
async def refresh_jwt(
    user: User = Depends(auth_user.get_current_auth_user_for_refresh),
):
    return await auth_user.get_access_token_via_refresh(user)


@router.post("/logout", response_model=LogoutMessage)
async def logout(response: Response):
    return await auth_user.handle_logout(response)
