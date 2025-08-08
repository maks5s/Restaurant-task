from pydantic import BaseModel, Field
import datetime

from app.core.schemas.dish import DishReadSchema
from app.core.models import Menu


class MenuSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=50)
    date: datetime.date


class MenuCreateSchema(MenuSchema):
    dish_ids: list[int]


class MenuReadSchema(MenuSchema):
    id: int
    restaurant_id: int
    dishes: list[DishReadSchema]

    @staticmethod
    def to_schema(menu: Menu):
        return MenuReadSchema(
            id=menu.id,
            title=menu.title,
            date=menu.date,
            restaurant_id=menu.restaurant_id,
            dishes=[DishReadSchema.from_orm(md.dish) for md in menu.menu_dishes if md.dish is not None]
        )


class MenuVotesSchema(BaseModel):
    menu: MenuReadSchema
    votes: int


class LegacyMenuVotesSchema(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=50)
    date: datetime.date
    restaurant_id: int
    dishes_list: list[DishReadSchema]
    votes_count: int
