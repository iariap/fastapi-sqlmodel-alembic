import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_get_songs(api_client: TestClient):
    result = api_client.get("/songs")
    result.raise_for_status()
    result = result.json()
    assert len(result["items"]) == 0
    assert result["total"] == 0
    assert result["limit"] == 50
    assert result["offset"] == 0
