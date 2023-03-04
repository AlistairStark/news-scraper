from fastapi import APIRouter

from app.controllers.ping import router as ping_router
from app.controllers.scrape_controller import router as scrape_router
from app.controllers.search_controller import router as search_router
from app.controllers.search_locations_controller import \
    router as search_locations_router
from app.controllers.search_terms_controller import \
    router as search_terms_router
from app.controllers.user_controller import router as user_router

v1_router = APIRouter()

v1_router.include_router(ping_router, tags=["ping"])
v1_router.include_router(user_router, tags=["user"])
v1_router.include_router(search_router, tags=["search"])
v1_router.include_router(search_terms_router, tags=["search terms"])
v1_router.include_router(search_locations_router, tags=["search locations"])
v1_router.include_router(scrape_router, tags=["scrape"])
