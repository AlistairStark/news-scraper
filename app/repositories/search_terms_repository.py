from typing import Sequence

from sqlalchemy import select
from app.models.schema import Search, SearchTerm
from app.repositories.base import DBRepository
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio.result import AsyncResult


class SearchTermRepository(DBRepository[Search]):
    Model = SearchTerm

    async def get_all_by_user_id(self, user_id: str) -> Sequence[Search]:
        session: AsyncSession
        async with self.session as session:
            stmt = select(Search).filter_by(user_id=user_id)
            r: AsyncResult = await session.execute(stmt)
            return r.scalars().all()

    async def create_search_terms(
        self,
        search_id: str,
        terms: Sequence[str],
    ) -> Sequence[SearchTerm]:
        session: AsyncSession
        async with self.session as session:
            terms = [SearchTerm(term=t, search_id=search_id) for t in terms]
            session.add_all(terms)
            await session.commit()
            return terms
