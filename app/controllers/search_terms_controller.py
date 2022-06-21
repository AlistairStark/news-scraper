from http import HTTPStatus
import logging
from typing import List, Sequence
from fastapi import APIRouter, Depends
from app.dependencies.db import get_db
from app.dependencies.auth import auth_schema
from app.models.schema import User
from app.services.search_service import SearchService
from app.validators import (
    CreateSearchTermsSchema,
    SearchTermsSchema,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/search-terms",
    status_code=HTTPStatus.CREATED,
    response_model=Sequence[SearchTermsSchema],
)
async def post_search(
    data: CreateSearchTermsSchema,
    user: User = Depends(auth_schema),
    db_session=Depends(get_db),
):
    """Create search terms for a search"""
    return await SearchService(db_session).create_search_terms(user, data)
