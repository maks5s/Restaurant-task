from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Employee, Restaurant
from core.schemas.vote import VoteReadSchema, VoteCreateSchema
from crud import vote as crud_vote
from crud import restaurant as crud_restaurant
from auth import user as auth_user


router = APIRouter(tags=["Votes"])


@router.post("/{restaurant_id}/votes", response_model=VoteReadSchema)
async def vote_for_menu(
    data: VoteCreateSchema,
    restaurant_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    employee: Employee = Depends(auth_user.get_employee_for_restaurant),
    restaurant: Restaurant = Depends(crud_restaurant.check_restaurant_exists)
):
    return await crud_vote.vote_for_menu(data, restaurant_id, employee, session)

