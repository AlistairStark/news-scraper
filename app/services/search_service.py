from http import HTTPStatus
from typing import List, Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.schema import Search, SearchLocation, SearchTerm, User
from app.repositories.search_location_repository import SearchLocationRepository
from app.repositories.search_repository import SearchRepository
from app.repositories.search_terms_repository import SearchTermRepository
from app.validators import (
    CreateSearchLocationsSchema,
    CreateSearchSchema,
    CreateSearchTermsSchema,
    UpdateSearchSchema,
)


class SearchService:
    def __init__(self, db_session: AsyncSession):
        self.search_repository = SearchRepository(db_session)
        self.search_terms_repository = SearchTermRepository(db_session)
        self.search_location_repository = SearchLocationRepository(db_session)

    def _split_ids(self, ids: str) -> List[int]:
        """Split a string of ids separated by ,"""
        try:
            return [int(id) for id in ids.split(",")]
        except Exception:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "invalid term IDs")

    async def create_search(self, user: User, data: CreateSearchSchema):
        await self.search_repository.create(
            **data.dict(),
            user_id=user.id,
        )

    async def get_by_id(
        self,
        user: User,
        search_id: str,
        include_relations=False,
    ) -> Search:

        search = await self.search_repository.get_by_id(
            search_id,
            include_relations=include_relations,
        )
        if not search or search.user_id != user.id:
            raise HTTPException(HTTPStatus.NOT_FOUND, "Search not found")
        return search

    async def delete_by_id(self, user: User, search_id: str) -> Search:
        search = await self.get_by_id(user, search_id)
        await self.search_repository.delete(search)

    async def update_search(self, user: User, data: UpdateSearchSchema):
        search = await self.get_by_id(user, data.id)
        await self.search_repository.update(search, **data.dict())

    async def get_searches_by_user(self, user: User) -> Sequence[Search]:
        return await self.search_repository.get_all_by_user_id(user.id)

    async def create_search_terms(
        self,
        user: User,
        data: CreateSearchTermsSchema,
    ) -> Sequence[SearchTerm]:
        search = await self.get_by_id(user, data.search_id)
        return await self.search_terms_repository.create_search_terms(
            search.id,
            data.terms,
        )

    async def delete_search_terms(self, user: User, term_ids_str: str, search_id: int):
        term_ids = self._split_ids(term_ids_str)
        await self.get_by_id(user, search_id)
        await self.search_terms_repository.delete_multiple(search_id, term_ids)

    async def create_search_locations(
        self, user: User, data: CreateSearchLocationsSchema
    ) -> Sequence[SearchLocation]:
        await self.get_by_id(user, data.search_id)
        return await self.search_location_repository.create_search_locations(
            data.search_id,
            data.locations,
        )

    async def delete_search_locations(
        self,
        user: User,
        term_ids_str: str,
        search_id: int,
    ):
        term_ids = self._split_ids(term_ids_str)
        await self.get_by_id(user, search_id)
        await self.search_location_repository.delete_multiple(search_id, term_ids)
