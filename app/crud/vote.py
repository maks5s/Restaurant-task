import datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Employee, Vote
from app.core.schemas.vote import VoteCreateSchema
from app.crud import menu as crud_menu


async def get_vote_by_employee_and_date(
    employee_id: int,
    vote_date: datetime.date,
    session: AsyncSession
):
    result = await session.execute(
        select(Vote)
        .where(
            Vote.employee_id == employee_id,
            Vote.vote_date == vote_date
        )
    )

    return result.scalar_one_or_none()


async def vote_for_menu(
    data: VoteCreateSchema,
    restaurant_id: int,
    employee: Employee,
    session: AsyncSession,
):
    today = datetime.date.today()

    target_menu = await crud_menu.get_menu_by_id(data.menu_id, session)
    if not target_menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu not found"
        )

    if target_menu.date != today:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only vote for today's menus"
        )

    existing_vote = await get_vote_by_employee_and_date(employee.id, today, session)
    if existing_vote:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already voted today"
        )

    vote = Vote(
        employee_id=employee.id,
        menu_id=data.menu_id,
        vote_date=today
    )

    session.add(vote)
    await session.commit()
    await session.refresh(vote)

    return vote
