import logging
from typing import Any

from fastapi import APIRouter, Depends

from app.dependencies.auth import auth_schema
from app.dependencies.db import get_db
from app.services.user_service import UserService
from app.validators import CreateUserSchema, UserSchema

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/user/create")
async def post_user_create(body: CreateUserSchema, db_session=Depends(get_db)):
    """Create a new user"""
    await UserService(db_session).create_user(body)
    return "", 201


@router.post("/user/login")
async def login(body: UserSchema, db_session=Depends(get_db)):
    """Login and generate token"""
    return await UserService(db_session).login(email=body.email, password=body.password)


@router.get("/user/test")
async def test(user: Any = Depends(auth_schema)):
    """Test a user has access"""
    return user.id
