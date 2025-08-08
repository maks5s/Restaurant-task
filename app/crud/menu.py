import datetime

from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.config import settings
from core.models import Menu, Dish, MenuDish, Vote
from core.schemas.dish import DishReadSchema
from core.schemas.menu import MenuCreateSchema, MenuReadSchema, MenuVotesSchema, LegacyMenuVotesSchema


async def get_menu_by_id(
    menu_id: int,
    session: AsyncSession,
):
    result = await session.execute(
        select(Menu).where(Menu.id == menu_id)
    )
    return result.scalar_one_or_none()


async def create_menu(
    data: MenuCreateSchema,
    restaurant_id: int,
    session: AsyncSession,
):
    if not data.dish_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Menu must contain at least one dish"
        )

    result = await session.execute(
        select(Dish)
        .where(Dish.id.in_(data.dish_ids), Dish.restaurant_id == restaurant_id)
    )
    dishes = result.scalars().all()

    if len(dishes) != len(set(data.dish_ids)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Some dishes do not exist or do not belong to this restaurant"
        )

    menu = Menu(
        title=data.title,
        date=data.date,
        restaurant_id=restaurant_id
    )
    session.add(menu)
    await session.flush()

    for dish in dishes:
        session.add(MenuDish(menu_id=menu.id, dish_id=dish.id))

    await session.commit()

    result = await session.execute(
        select(Menu)
        .options(joinedload(Menu.menu_dishes).joinedload(MenuDish.dish))
        .where(Menu.id == menu.id)
    )
    return result.unique().scalar_one()


async def get_menus_by_date(
    restaurant_id: int,
    date: datetime.date,
    session: AsyncSession,
):
    query_date = date or datetime.date.today()

    result = await session.execute(
        select(Menu)
        .options(joinedload(Menu.menu_dishes).joinedload(MenuDish.dish))
        .where(Menu.restaurant_id == restaurant_id, Menu.date == query_date)
    )
    menus = result.scalars().unique().all()

    return menus


async def get_current_menu(
    restaurant_id: int,
    session: AsyncSession
):
    today = datetime.date.today()

    result = await session.execute(
        select(
            Menu,
            func.count(Vote.id).label("vote_count")
        )
        .outerjoin(Vote, Menu.id == Vote.menu_id)
        .options(joinedload(Menu.menu_dishes).joinedload(MenuDish.dish))
        .where(Menu.date == today, Menu.restaurant_id == restaurant_id)
        .group_by(Menu.id)
        .order_by(func.count(Vote.id).desc())
        .limit(1)
    )

    row = result.first()

    if row is None:
        return None

    menu, vote_count = row

    return menu


async def get_day_results(
    restaurant_id: int,
    session: AsyncSession,
    app_version: str
):
    today = datetime.date.today()

    result = await session.execute(
        select(
            Menu,
            func.count(Vote.id).label("vote_count")
        )
        .outerjoin(Vote, Menu.id == Vote.menu_id)
        .options(joinedload(Menu.menu_dishes).joinedload(MenuDish.dish))
        .where(Menu.date == today, Menu.restaurant_id == restaurant_id)
        .group_by(Menu.id)
        .order_by(func.count(Vote.id).desc())
    )

    rows = result.unique().all()

    if not rows:
        return []

    # Different responses based on user`s app version
    if settings.is_legacy(app_version):
        return (
            [LegacyMenuVotesSchema(
                id=menu.id,
                name=menu.title,
                date=menu.date,
                restaurant_id=menu.restaurant_id,
                dishes_list=[DishReadSchema.from_orm(md.dish) for md in menu.menu_dishes if md.dish is not None],
                votes_count=vote_count
            ) for menu, vote_count in rows]
        )
    else:
        return (
            [MenuVotesSchema(
                menu=MenuReadSchema.to_schema(menu),
                votes=vote_count
            ) for menu, vote_count in rows]
        )
