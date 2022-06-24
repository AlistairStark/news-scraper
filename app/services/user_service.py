from __future__ import annotations

from http import HTTPStatus
from typing import Dict

import bcrypt
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schema import User
from app.repositories.user_repository import UserRepository
from app.services.token_service import TokenService
from app.validators import CreateUserSchema


class UserService(object):
    def __init__(self, db_session: AsyncSession):
        self.user_repository = UserRepository(db_session)
        self.token_service = TokenService()

    def _hash_password(self, password: str) -> str:
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt(rounds=10)
        )
        return hashed_password.decode("utf-8")

    def _check_password(self, user: User, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8"))

    async def _get_user_by_email(self, email: str) -> User:
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise HTTPException(
                HTTPStatus.NOT_FOUND, f"User with email {email} not found"
            )
        return user

    async def create_user(self, body: CreateUserSchema):
        password = self._hash_password(body.password)
        await self.user_repository.create_user(body.email, password)

    async def login(self, email: str, password: str) -> Dict:
        user = await self._get_user_by_email(email)
        if not self._check_password(user, password):
            raise HTTPException(HTTPStatus.FORBIDDEN, f"Email or password is incorrect")
        token = self.token_service.create_token(identity=user.email)
        return dict(token=token)
