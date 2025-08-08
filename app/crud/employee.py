from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.models import Employee
from core.schemas.employee import EmployeeCreateSchema
from crud import user as crud_user


async def get_employee_by_user_and_restaurant(
    session: AsyncSession,
    user_id: int,
    restaurant_id: int,
):
    result = await session.execute(
        select(Employee).where(
            Employee.user_id == user_id,
            Employee.restaurant_id == restaurant_id
        )
    )
    return result.scalar_one_or_none()


async def get_employee_with_user(
    session: AsyncSession,
    employee_id: int,
):
    result = await session.execute(
        select(Employee)
        .options(joinedload(Employee.user))
        .where(Employee.id == employee_id)
    )
    return result.scalar_one_or_none()


async def create_employee(
    data: EmployeeCreateSchema,
    restaurant_id: int,
    session: AsyncSession,
):
    target_user = await crud_user.get_user_by_id(session, data.user_id)
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    existing_employee = await get_employee_by_user_and_restaurant(
        session=session,
        user_id=data.user_id,
        restaurant_id=restaurant_id,
    )
    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This user is already an employee of the restaurant",
        )

    employee = Employee(
        is_admin=False,
        user_id=data.user_id,
        restaurant_id=restaurant_id,
    )

    session.add(employee)
    await session.commit()
    await session.refresh(employee)

    return await get_employee_with_user(session, employee.id)
