from datetime import datetime
from typing import List

from sqlalchemy import and_, or_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio.result import AsyncResult
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.schema import Result
from app.repositories.base import DBRepository


class ResultRepository(DBRepository[Result]):
    Model = Result

    async def upsert_results(self, results: List[dict]):
        if len(results) < 1:
            return
        session: AsyncSession
        async with self.session as session:
            stmt = insert(Result).values(results)
            stmt = stmt.on_conflict_do_update(
                constraint="unique_link_search",
                set_={"updated_at": datetime.now()},
            )
            await session.execute(stmt)
            await session.commit()
            await session.flush()

    async def get_results(
        self,
        search_id: int,
        start: datetime,
        end: datetime,
        include_previous=False,
    ) -> List[Result]:
        session: AsyncSession
        async with self.session as session:
            stmt = select(Result).filter_by(search_id=search_id)
            if include_previous:
                stmt = stmt.filter(
                    or_(
                        and_(
                            Result.updated_at >= start,
                            Result.updated_at <= end,
                        ),
                        and_(
                            Result.created_at >= start,
                            Result.created_at <= end,
                        ),
                    )
                )
            else:
                stmt = stmt.filter(
                    Result.created_at >= start,
                    Result.created_at <= end,
                )
            stmt = stmt.order_by(Result.agency)
            r: AsyncResult = await session.execute(stmt)
            return r.scalars().all()
