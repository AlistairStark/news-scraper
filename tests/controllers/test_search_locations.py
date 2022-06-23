from http import HTTPStatus

import pytest
from sqlalchemy import select
from starlette.testclient import TestClient

from app.models.schema import SearchLocation


@pytest.mark.asyncio
async def test_create_search_locations(
    client: TestClient,
    override_auth,
    db_session,
    search,
):
    search_id = search.id
    data = dict(
        locations=[
            {"url": "www.term1.com", "name": "test1"},
            {"url": "www.term2.com", "name": "test2"},
            {"url": "www.term3.com", "name": "test3"},
        ],
        search_id=search_id,
    )
    r = await client.post("/v1/search-location", json=data)
    assert r.status_code == HTTPStatus.CREATED
    expected_length = 3
    got_result_len = len(r.json())
    assert expected_length == got_result_len
    async with db_session as session:
        stmt = select(SearchLocation).filter_by(search_id=search_id)
        r = await session.execute(stmt)
        got_len = len(r.scalars().all())
        assert got_len == expected_length


@pytest.mark.asyncio
async def test_delete_search_locations(
    client: TestClient,
    override_auth,
    db_session,
    search,
    search_locations,
):
    search_id = search.id
    ids = ",".join([str(t.id) for t in search_locations])
    params = dict(ids=ids, search_id=search_id)
    r = await client.delete("/v1/search-location", params=params)
    assert r.status_code == HTTPStatus.NO_CONTENT
    expected_length = 0
    async with db_session as session:
        stmt = select(SearchLocation).filter_by(search_id=search_id)
        r = await session.execute(stmt)
        got_len = len(r.scalars().all())
        assert got_len == expected_length
