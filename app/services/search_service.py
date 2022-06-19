from sqlalchemy.ext.asyncio.session import AsyncSession
from app.models.schema import User

from app.repositories.search_repository import SearchRepository
from app.validators import CreateSearchSchema


class SearchService:
    def __init__(self, db_session: AsyncSession):
        self.search_repository = SearchRepository(db_session)

    async def create_search(self, user: User, data: CreateSearchSchema):
        await self.search_repository.create(
            name=data.name,
            description=data.description,
            is_rss=data.is_rss,
            user_id=user.id,
        )
