from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper, Employee, Restaurant
from app.core.schemas.vote import VoteReadSchema, VoteCreateSchema
from app.crud import vote as crud_vote
from app.crud import restaurant as crud_restaurant
from app.auth import user as auth_user


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

