import logging
from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer

from app import settings
from app.dependencies.auth import auth_schema
from app.dependencies.db import get_db
from app.models.schema import User
from app.services.user_service import UserService
from app.validators import CreateUserSchema, UserSchema

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/user/create")
async def post_user_create(body: CreateUserSchema, db_session=Depends(get_db)):
    """Create a new user"""
    if body.create_secret != settings.CREATE_SECRET:
        raise HTTPException(HTTPStatus.FORBIDDEN, "Get outta here!")
    await UserService(db_session).create_user(body)
    return "", 201


@router.post("/user/login")
async def login(body: UserSchema, db_session=Depends(get_db)):
    """Login and generate token"""
    return await UserService(db_session).login(email=body.email, password=body.password)


@router.get("/user/test")
async def test(user: Any = Depends(auth_schema)):
    """Login and generate token"""
    return user.id
