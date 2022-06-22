from http import HTTPStatus
import logging
from typing import Sequence
from fastapi import APIRouter, Depends
from app.dependencies.db import get_db
from app.dependencies.auth import auth_schema
from app.models.schema import User
from app.services.search_service import SearchService
from app.validators import (
    CreateSearchSchema,
    SearchSchema,
    SearchWithTermsLocations,
    UpdateSearchSchema,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/search", status_code=HTTPStatus.CREATED)
async def post_search(
    data: CreateSearchSchema,
    user: User = Depends(auth_schema),
    db_session=Depends(get_db),
):
    """Create a search"""
    await SearchService(db_session).create_search(user, data)


@router.get(
    "/search", status_code=HTTPStatus.OK, response_model=SearchWithTermsLocations
)
async def get_search(
    search_id: int,
    user: User = Depends(auth_schema),
    db_session=Depends(get_db),
):
    """Get a search by ID"""
    return await SearchService(db_session).get_by_id(
        user,
        search_id,
        include_relations=True,
    )


@router.delete("/search", status_code=HTTPStatus.NO_CONTENT)
async def delete_search(
    search_id: int,
    user: User = Depends(auth_schema),
    db_session=Depends(get_db),
):
    """Delete a search by ID"""
    return await SearchService(db_session).delete_by_id(user, search_id)


@router.put("/search", status_code=HTTPStatus.OK)
async def update_search(
    data: UpdateSearchSchema,
    user: User = Depends(auth_schema),
    db_session=Depends(get_db),
):
    """Delete a search by ID"""
    return await SearchService(db_session).update_search(user, data)


@router.get(
    "/search-all",
    status_code=HTTPStatus.OK,
    response_model=Sequence[SearchSchema],
)
async def get_search(
    user: User = Depends(auth_schema),
    db_session=Depends(get_db),
):
    """Get a search by ID"""
    return await SearchService(db_session).get_searches_by_user(user)
