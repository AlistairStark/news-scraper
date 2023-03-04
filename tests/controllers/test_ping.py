import pytest
from starlette.testclient import TestClient


@pytest.mark.asyncio
async def test_create_flow(client: TestClient):
    r = await client.post("/v1/ping")

    got = r.json()
    expected = "pong"

    assert r.status_code == 200
    assert got == expected
