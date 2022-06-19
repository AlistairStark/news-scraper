from datetime import datetime, timezone
from http import HTTPStatus
from typing import Optional
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from app.models.schema import User
from app.repositories.user_repository import UserRepository
from app.services.token_service import TokenService
from app.session import async_session


class Auth(HTTPBearer):
    def __init__(self, token_service: TokenService = TokenService()):
        super().__init__()
        self.token_service = token_service

    def _parse_token(self, token) -> str:
        try:
            token = self.token_service.decode_token(token)
        except Exception:
            raise HTTPException(HTTPStatus.FORBIDDEN, "Invalid token")
        now = datetime.now(timezone.utc)
        if token.expiry < now:
            raise HTTPException(HTTPStatus.FORBIDDEN, "Expired token")
        return token.identity

    async def _get_user(self, user_email: str) -> User:
        async with async_session() as session:
            user = await UserRepository(session).get_by_email(user_email)
            if not user:
                raise HTTPException(HTTPStatus.FORBIDDEN, "Invalid user")
            return user

    async def __call__(self, request: Request) -> Optional[User]:
        r = await super().__call__(request)
        user_email = self._parse_token(r.credentials)
        user = await self._get_user(user_email)
        return user


auth_schema = Auth()
