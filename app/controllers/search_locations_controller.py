from http import HTTPStatus
import logging
from typing import Sequence
from fastapi import APIRouter, Depends
from app.dependencies.db import get_db
from app.dependencies.auth import auth_schema
from app.models.schema import User
from app.services.search_service import SearchService
from app.validators import (
    CreateSearchLocationsSchema,
    SearchLocationsSchema,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/search-location",
    status_code=HTTPStatus.CREATED,
    response_model=Sequence[SearchLocationsSchema],
)
async def post_search_terms(
    data: CreateSearchLocationsSchema,
    user: User = Depends(auth_schema),
    db_session=Depends(get_db),
):
    """Create search terms for a search"""
    return await SearchService(db_session).create_search_locations(user, data)


# @bp.post("/search-location")
# @jwt_required()
# def post_search_locations():
#     body: CreateSearchLocations = deserialize_body(
#         CreateSearchLocationsSchema, CreateSearchLocations
#     )
#     locations = SearchService().create_search_locations(current_user.id, body)
#     return jsonify(locations)
