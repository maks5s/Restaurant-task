from pydantic import BaseModel, Field


class RestaurantSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: str | None = Field(None, min_length=1, max_length=255)


class RestaurantCreateSchema(RestaurantSchema):
    pass


class RestaurantReadSchema(RestaurantSchema):
    id: int
