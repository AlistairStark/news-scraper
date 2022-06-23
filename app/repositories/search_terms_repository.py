from typing import Sequence

from sqlalchemy import delete
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.schema import SearchTerm
from app.repositories.base import DBRepository


class SearchTermRepository(DBRepository[SearchTerm]):
    Model = SearchTerm

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

    async def delete_multiple(self, search_id: int, term_ids: Sequence[int]):
        session: AsyncSession
        async with self.session as session:
            stmt = delete(SearchTerm).where(
                SearchTerm.id.in_(term_ids),
                SearchTerm.search_id == search_id,
            )
            await session.execute(stmt)
            await session.commit()
