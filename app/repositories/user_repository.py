from __future__ import annotations

from typing import List

from pyparsing import Optional
from sqlalchemy.ext.asyncio.result import AsyncResult
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select

from app.models import User
from app.repositories.base import DBRepository


class UserRepository(DBRepository[User]):
    Model = User

    async def get_all(self) -> List[User]:
        session: AsyncSession
        async with self.session as session:
            result: AsyncResult = await session.execute(select(User))
            return result.scalars().all()

    async def create_user(self, email: str, password: str):
        async with self.session as session:
            u = User(email=email, password=password)
            session.add(u)
            await session.commit()

    async def get_by_email(self, email: str) -> Optional[User]:
        async with self.session as session:
            result: AsyncResult = await session.execute(
                select(User).where(User.email == email)
            )
            return result.scalar_one_or_none()
