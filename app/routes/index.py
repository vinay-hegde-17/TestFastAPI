#main.py for register all routes

from fastapi import APIRouter
from app.routes.users import router as user_router
from app.routes.items import router as item_router
from app.routes.orders import router as order_router

router = APIRouter()

router.include_router(user_router)
router.include_router(item_router)
router.include_router(order_router)
