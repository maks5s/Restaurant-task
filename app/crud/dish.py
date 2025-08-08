from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Dish
from core.schemas.dish import DishCreateSchema


async def get_dish_by_name_and_restaurant(
    session: AsyncSession,
    name: str,
    restaurant_id: int,
):
    result = await session.execute(
        select(Dish).where(
            Dish.name == name,
            Dish.restaurant_id == restaurant_id
        )
    )
    return result.scalar_one_or_none()


async def create_dish(
    data: DishCreateSchema,
    restaurant_id: int,
    session: AsyncSession,
):
    existing_dish = await get_dish_by_name_and_restaurant(
        session=session,
        name=data.name,
        restaurant_id=restaurant_id,
    )
    if existing_dish:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dish with this name already exists in this restaurant",
        )

    dish = Dish(
        name=data.name,
        description=data.description,
        restaurant_id=restaurant_id,
    )

    session.add(dish)
    await session.commit()
    await session.refresh(dish)

    return dish
