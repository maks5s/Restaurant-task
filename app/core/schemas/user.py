from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)


class UserPasswordSchema(UserSchema):
    password: str = Field(..., min_length=5)


class UserReadSchema(UserSchema):
    id: int
