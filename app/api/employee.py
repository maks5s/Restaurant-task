from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper, Employee, Restaurant
from app.core.schemas.employee import EmployeeCreateSchema, EmployeeReadSchema
from app.crud import employee as crud_employee
from app.crud import restaurant as crud_restaurant
from app.auth import user as auth_user


router = APIRouter(tags=["Employees"])


@router.post("/{restaurant_id}/employees", response_model=EmployeeReadSchema)
async def add_employee(
    data: EmployeeCreateSchema,
    restaurant_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    admin: Employee = Depends(auth_user.get_admin_employee_for_restaurant),
    restaurant: Restaurant = Depends(crud_restaurant.check_restaurant_exists)
):
    return await crud_employee.create_employee(data, restaurant_id, session)