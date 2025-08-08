from fastapi import HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User, Restaurant, Employee, db_helper
from app.core.schemas.restaurant import RestaurantCreateSchema


async def check_restaurant_exists(
    restaurant_id: int,
    session: AsyncSession = Depends(db_helper.session_getter)
):
    target_restaurant = await get_restaurant_by_id(session, restaurant_id)
    if not target_restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    return target_restaurant


async def get_restaurant_by_name(
    session: AsyncSession,
    name: str,
):
    result = await session.execute(
        select(Restaurant).where(Restaurant.name == name)
    )
    return result.scalar_one_or_none()


async def get_restaurant_by_id(
    session: AsyncSession,
    restaurant_id: int,
):
    result = await session.execute(
        select(Restaurant).where(Restaurant.id == restaurant_id)
    )
    return result.scalar_one_or_none()


async def create_restaurant(
    data: RestaurantCreateSchema,
    user: User,
    session: AsyncSession,
):
    existing = await get_restaurant_by_name(session, data.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Restaurant with this name already exists"
        )

    restaurant = Restaurant(
        name=data.name,
        description=data.description,
    )
    session.add(restaurant)
    await session.flush()

    employee = Employee(
        is_admin=True,
        user_id=user.id,
        restaurant_id=restaurant.id,
    )
    session.add(employee)
    await session.commit()
    await session.refresh(restaurant)

    return restaurant
