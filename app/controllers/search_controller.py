from http import HTTPStatus
import logging
from fastapi import APIRouter, Depends
from app.dependencies.db import get_db
from app.dependencies.auth import auth_schema
from app.models.schema import User
from app.services.search_service import SearchService
from app.validators import CreateSearchSchema

logger = logging.getLogger(__name__)

router = APIRouter()



@router.post("/search")
async def post_search(data: CreateSearchSchema, user: User =Depends(auth_schema), db_session=Depends(get_db)):
    """Create a search"""
    await SearchService(db_session).create_search(user, data)
    return "", HTTPStatus.CREATED
