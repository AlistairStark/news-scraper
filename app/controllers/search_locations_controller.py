import logging
from http import HTTPStatus
from typing import Sequence

from fastapi import APIRouter, Depends

from app.dependencies.auth import auth_schema
from app.dependencies.db import get_db
from app.models.schema import User
from app.services.search_service import SearchService
from app.validators import CreateSearchLocationsSchema, SearchLocationsSchema

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/search-location",
    status_code=HTTPStatus.CREATED,
    response_model=Sequence[SearchLocationsSchema],
)
async def post_search_locations(
    data: CreateSearchLocationsSchema,
    user: User = Depends(auth_schema),
    db_session=Depends(get_db),
):
    """Create search locations for a search"""
    return await SearchService(db_session).create_search_locations(user, data)


@router.delete("/search-location", status_code=HTTPStatus.NO_CONTENT)
async def delete_search_locations(
    ids: str,
    search_id: int,
    user: User = Depends(auth_schema),
    db_session=Depends(get_db),
):
    """Delete search locations for a search"""
    return await SearchService(db_session).delete_search_locations(user, ids, search_id)
