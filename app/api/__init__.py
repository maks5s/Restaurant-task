from fastapi import APIRouter

from app.core.config import settings
from .auth import router as auth_router
from .restaurant import router as restaurant_router


router = APIRouter(prefix=settings.api.prefix)
router.include_router(auth_router)
router.include_router(restaurant_router)
