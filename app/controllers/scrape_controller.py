import logging

from fastapi import APIRouter, Depends

from app.dependencies.auth import auth_schema
from app.dependencies.db import get_db
from app.models.schema import User
from app.services.scraper_service import ScraperService
from app.services.search_service import SearchService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/scrape")
async def get_scrape_data(
    search_id: int,
    include_previous: bool,
    user: User = Depends(auth_schema),
    db_session=Depends(get_db),
):
    """Scrape Data"""
    search = await SearchService(db_session).get_by_id(
        user,
        search_id,
        include_relations=True,
    )
    r = await ScraperService(db_session, search).scrape_sites(include_previous)
    return {"links": r}
