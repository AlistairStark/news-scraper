from http import HTTPStatus
from typing import Sequence
from fastapi import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.models.schema import Search, SearchTerm, User

from app.repositories.search_repository import SearchRepository
from app.repositories.search_terms_repository import SearchTermRepository
from app.validators import (
    CreateSearchSchema,
    CreateSearchTermsSchema,
    UpdateSearchSchema,
)


class SearchService:
    def __init__(self, db_session: AsyncSession):
        self.search_repository = SearchRepository(db_session)
        self.search_terms_repository = SearchTermRepository(db_session)

    async def create_search(self, user: User, data: CreateSearchSchema):
        await self.search_repository.create(
            **data.dict(),
            user_id=user.id,
        )

    async def get_by_id(self, user: User, search_id: str) -> Search:
        search = await self.search_repository.get_by_id(search_id)
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
