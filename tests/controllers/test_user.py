import pytest
from starlette.testclient import TestClient


@pytest.mark.asyncio
async def test_create_flow(client: TestClient, override_auth):
    r = await client.get("/v1/user/test")

    got = r.json()
    expected = override_auth.id

    assert r.status_code == 200
    assert got == expected
