from fastapi import APIRouter

from app.controllers.ping import router as ping_router
from app.controllers.user_controller import router as user_router
from app.controllers.search_controller import router as search_router

v1_router = APIRouter()

v1_router.include_router(ping_router, tags=["ping"])
v1_router.include_router(user_router, tags=["user"])
v1_router.include_router(search_router, tags=['search'])
