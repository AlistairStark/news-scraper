from http import HTTPStatus
import pytest
from starlette.testclient import TestClient

from app.models.schema import Search


@pytest.mark.asyncio
async def test_create_search(
    client: TestClient,
    override_auth,
    db_session,
):
    data = dict(
        name="testsearch",
        description="this is a test search",
        is_rss=True,
    )
    r = await client.post("/v1/search", json=data)
    assert r.status_code == HTTPStatus.CREATED

    async with db_session as session:
        r = await session.get(Search, 1)
        assert r is not None
