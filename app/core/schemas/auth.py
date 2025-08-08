from pydantic import BaseModel, Field

from core.schemas.user import UserPasswordSchema


class LoginSchema(UserPasswordSchema):
    pass


class RegisterSchema(LoginSchema):
    confirm_password: str = Field(..., min_length=5)


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class LogoutMessage(BaseModel):
    message: str
