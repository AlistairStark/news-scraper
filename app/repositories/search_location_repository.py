from typing import Sequence

from sqlalchemy import delete
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.schema import SearchLocation, SearchTerm
from app.repositories.base import DBRepository
from app.validators import LocationSchema


class SearchLocationRepository(DBRepository[SearchLocation]):
    Model = SearchLocation

    async def create_search_locations(
        self,
        search_id: int,
        locations: Sequence[LocationSchema],
    ) -> Sequence[SearchTerm]:
        session: AsyncSession
        async with self.session as session:
            locations = [
                SearchLocation(
                    name=l.name,
                    url=l.url,
                    search_id=search_id,
                )
                for l in locations
            ]
            session.add_all(locations)
            await session.commit()
            return locations

    async def delete_multiple(self, search_id: int, term_ids: Sequence[int]):
        session: AsyncSession
        async with self.session as session:
            stmt = delete(SearchLocation).where(
                SearchLocation.id.in_(term_ids),
                SearchLocation.search_id == search_id,
            )
            await session.execute(stmt)
            await session.commit()
