from typing import Sequence

from sqlalchemy import select
from app.models.schema import Search
from app.repositories.base import DBRepository
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio.result import AsyncResult


class SearchRepository(DBRepository[Search]):
    Model = Search

    async def get_all_by_user_id(self, user_id: str) -> Sequence[Search]:
        session: AsyncSession
        async with self.session as session:
            stmt = select(Search).filter_by(user_id=user_id)
            r: AsyncResult = await session.execute(stmt)
            return r.scalars().all()