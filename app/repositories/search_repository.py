from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio.result import AsyncResult
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.schema import Search
from app.repositories.base import DBRepository


class SearchRepository(DBRepository[Search]):
    Model = Search

    async def get_all_by_user_id(self, user_id: str) -> Sequence[Search]:
        session: AsyncSession
        async with self.session as session:
            stmt = select(Search).filter_by(user_id=user_id)
            r: AsyncResult = await session.execute(stmt)
            return r.scalars().all()

    async def get_by_id(
        self,
        search_id: str,
        include_relations=False,
    ) -> Optional[Search]:
        session: AsyncSession
        async with self.session as session:
            stmt = select(Search).filter_by(id=search_id)
            if include_relations:
                stmt = stmt.options(
                    joinedload(Search.search_locations),
                    joinedload(Search.search_terms),
                )
            r: AsyncResult = await session.execute(stmt)
            return r.unique().scalar_one_or_none()
