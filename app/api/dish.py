from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Employee, Restaurant
from core.schemas.dish import DishReadSchema, DishCreateSchema
from crud import dish as crud_dish
from crud import restaurant as crud_restaurant
from auth import user as auth_user


router = APIRouter(tags=["Dishes"])


@router.post("/{restaurant_id}/dishes", response_model=DishReadSchema)
async def add_dish(
    data: DishCreateSchema,
    restaurant_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    admin: Employee = Depends(auth_user.get_admin_employee_for_restaurant),
    restaurant: Restaurant = Depends(crud_restaurant.check_restaurant_exists)
):
    return await crud_dish.create_dish(data, restaurant_id, session)
