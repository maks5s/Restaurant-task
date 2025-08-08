from pydantic import BaseModel, Field


class DishSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: str | None = Field(None, min_length=1, max_length=255)


class DishCreateSchema(DishSchema):
    pass


class DishReadSchema(DishSchema):
    id: int
    restaurant_id: int

    class Config:
        from_attributes = True
