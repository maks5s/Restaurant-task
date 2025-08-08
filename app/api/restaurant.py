from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User
from core.schemas.restaurant import RestaurantReadSchema, RestaurantCreateSchema
from crud import restaurant as crud_restaurant
from auth import user as auth_user
from .dish import router as dish_router
from .employee import router as employee_router
from .menu import router as menu_router
from .vote import router as vote_router


router = APIRouter(prefix="/restaurants", tags=["Restaurants"])
router.include_router(dish_router)
router.include_router(employee_router)
router.include_router(menu_router)
router.include_router(vote_router)


@router.post("/", response_model=RestaurantReadSchema)
async def create_restaurant(
    data: RestaurantCreateSchema,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(auth_user.get_current_auth_user),
):
    return await crud_restaurant.create_restaurant(data, user, session)









