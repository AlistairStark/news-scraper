from datetime import datetime, timedelta
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.models.schema import Result

from app.repositories.result_repository import ResultRepository


@pytest.mark.asyncio
async def test_upsert_result(db_session: AsyncSession, search):
    search_id = search.id
    results = [
        {
            "agency": "site1",
            "title": "title1",
            "link": "link_text1",
            "search_id": search_id,
        },
        {
            "agency": "site2",
            "title": "title2",
            "link": "link_text2",
            "search_id": search_id,
        },
        {
            "agency": "site3",
            "title": "title3",
            "link": "link_text3",
            "search_id": search_id,
        },
    ]

    await ResultRepository(db_session).upsert_results(results)
    expected_len = 3
    async with db_session as session:
        stmt = select(Result).filter_by(search_id=search_id)
        r = await session.execute(stmt)
        got_len = len(r.scalars().all())
        assert got_len == expected_len


@pytest.mark.asyncio
async def test_upsert_result_overwrite(db_session: AsyncSession, search):
    search_id = search.id
    results = [
        {
            "agency": "site1",
            "title": "title1",
            "link": "link_text1",
            "search_id": search_id,
        },
        {
            "agency": "site2",
            "title": "title2",
            "link": "link_text2",
            "search_id": search_id,
        },
        {
            "agency": "site3",
            "title": "title3",
            "link": "link_text3",
            "search_id": search_id,
        },
    ]
    repository_service = ResultRepository(db_session)
    await repository_service.upsert_results(results)
    updated_at = datetime.now()
    async with db_session as session:
        stmt = select(Result).filter_by(search_id=search_id)
        r = await session.execute(stmt)
        results = r.scalars().all()
        got_len = len(results)
        for res in results:
            updated_at = res.updated_at
    expected_upsert_value = "upserted"
    results_2 = [
        {
            "agency": expected_upsert_value,
            "title": expected_upsert_value,
            "link": "link_text1",
            "search_id": search_id,
        },
        {
            "agency": expected_upsert_value,
            "title": expected_upsert_value,
            "link": "link_text2",
            "search_id": search_id,
        },
        {
            "agency": expected_upsert_value,
            "title": expected_upsert_value,
            "link": "link_text3",
            "search_id": search_id,
        },
    ]
    await repository_service.upsert_results(results_2)
    expected_len = 3
    async with db_session as session:
        stmt = select(Result).filter_by(search_id=search_id)
        r = await session.execute(stmt)
        results = r.scalars().all()
        got_len = len(results)
        assert got_len == expected_len
        for res in results:
            assert res.updated_at != updated_at


@pytest.mark.asyncio
async def test_get_result(db_session: AsyncSession, search, results):
    start = datetime.now() - timedelta(hours=1)
    end = start + timedelta(hours=2)
    results = await ResultRepository(db_session).get_results(
        search_id=search.id,
        start=start,
        end=end,
    )
    got_len = len(results)
    expected_len = 3
    assert got_len == expected_len
