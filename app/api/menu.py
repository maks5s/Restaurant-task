import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Employee, Restaurant
from core.schemas.menu import MenuReadSchema, MenuCreateSchema, MenuVotesSchema
from crud import menu as crud_menu
from crud import restaurant as crud_restaurant
from auth import user as auth_user


router = APIRouter(tags=["Menus"])


@router.post("/{restaurant_id}/menus", response_model=MenuReadSchema)
async def add_menu(
    data: MenuCreateSchema,
    restaurant_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    admin: Employee = Depends(auth_user.get_admin_employee_for_restaurant),
    restaurant: Restaurant = Depends(crud_restaurant.check_restaurant_exists)
):
    menu = await crud_menu.create_menu(data, restaurant_id, session)

    return MenuReadSchema.to_schema(menu)


@router.get("/{restaurant_id}/menus/current", response_model=MenuReadSchema)
async def get_current_menu(
    restaurant_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    employee: Employee = Depends(auth_user.get_employee_for_restaurant),
    restaurant: Restaurant = Depends(crud_restaurant.check_restaurant_exists)
):
    menu = await crud_menu.get_current_menu(restaurant_id, session)

    return MenuReadSchema.to_schema(menu)


@router.get("/{restaurant_id}/menus/results", response_model=list[MenuVotesSchema])
async def get_current_day_results(
    restaurant_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    employee: Employee = Depends(auth_user.get_employee_for_restaurant),
    restaurant: Restaurant = Depends(crud_restaurant.check_restaurant_exists)
):
    return await crud_menu.get_day_results(restaurant_id, session)


@router.get("/{restaurant_id}/menus", response_model=list[MenuReadSchema])
async def get_menus(
    restaurant_id: int,
    date: datetime.date | None = Query(None, description="Date to filter menus"),
    session: AsyncSession = Depends(db_helper.session_getter),
    employee: Employee = Depends(auth_user.get_employee_for_restaurant),
    restaurant: Restaurant = Depends(crud_restaurant.check_restaurant_exists)
):
    menus = await crud_menu.get_menus_by_date(restaurant_id, date, session)

    return (
        [MenuReadSchema.to_schema(menu) for menu in menus]
    )

