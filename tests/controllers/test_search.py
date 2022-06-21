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


@pytest.mark.asyncio
async def test_get_search(
    client: TestClient,
    override_auth,
    search,
):
    expected = dict(
        id=search.id,
        name=search.name,
        description=search.description,
        user_id=search.user_id,
        is_rss=search.is_rss,
    )
    data = dict(search_id=search.id)
    r = await client.get("/v1/search", params=data)
    assert r.status_code == HTTPStatus.OK

    got = r.json()
    assert got == expected


@pytest.mark.asyncio
async def test_delete_search(
    client: TestClient,
    override_auth,
    db_session,
    search,
):
    search_id = search.id
    data = dict(search_id=search_id)
    r = await client.delete("/v1/search", params=data)
    assert r.status_code == HTTPStatus.NO_CONTENT
    async with db_session as session:
        r = await session.get(Search, search_id)
        assert r is None


@pytest.mark.asyncio
async def test_update_search(
    client: TestClient,
    override_auth,
    db_session,
    search,
):
    search_id = search.id
    changed_name = "new name"
    data = dict(
        id=search_id,
        name=changed_name,
        description=search.description,
        is_rss=search.is_rss,
    )
    r = await client.put("/v1/search", json=data)
    assert r.status_code == HTTPStatus.OK
    async with db_session as session:
        r = await session.get(Search, search_id)
        assert r.id == search_id
        assert r.name == changed_name


@pytest.mark.asyncio
async def test_get_search_all(
    client: TestClient,
    override_auth,
    search,
):
    expected = [
        dict(
            id=search.id,
            name=search.name,
            description=search.description,
            user_id=search.user_id,
            is_rss=search.is_rss,
        )
    ]
    r = await client.get("/v1/search-all")
    assert r.status_code == HTTPStatus.OK

    got = r.json()
    assert got == expected
