from pydantic import BaseModel, Field

from core.schemas.user import UserSchema


class EmployeeSchema(BaseModel):
    user: UserSchema
    restaurant_id: int
    is_admin: bool = Field(False)


class EmployeeCreateSchema(BaseModel):
    user_id: int


class EmployeeReadSchema(EmployeeSchema):
    id: int
