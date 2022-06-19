import pytest
from starlette.testclient import TestClient


@pytest.mark.asyncio
async def test_create_flow(client: TestClient):
    r = await client.post(
        "/v1/ping",
        json={
            "name": "test flow",
            "short_code": "testcode",
            "description": "this is a test flow",
        },
    )

    got = r.json()
    expected = "hi"

    assert r.status_code == 200
    assert got == expected
