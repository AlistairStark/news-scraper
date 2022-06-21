from http import HTTPStatus
import pytest
from sqlalchemy import select
from starlette.testclient import TestClient

from app.models.schema import SearchTerm


@pytest.mark.asyncio
async def test_create_search_terms(
    client: TestClient,
    override_auth,
    db_session,
    search,
):
    search_id = search.id
    data = dict(
        terms=["term 1", "term 2", "term 3"],
        search_id=search_id,
    )
    r = await client.post("/v1/search-terms", json=data)
    assert r.status_code == HTTPStatus.CREATED
    expected_length = 3
    got_result_len = len(r.json())
    assert expected_length == got_result_len
    async with db_session as session:
        stmt = select(SearchTerm).filter_by(search_id=search_id)
        r = await session.execute(stmt)
        got_len = len(r.scalars().all())
        assert got_len == expected_length
