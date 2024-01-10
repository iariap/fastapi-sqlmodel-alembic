import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_create(api_client: TestClient):
    result = api_client.get("/songs")
    assert result
    assert result.status_code == 200

    result = result.json()
    assert len(result["items"]) == 0
    assert result["total"] == 0
    assert result["limit"] == 50
    assert result["offset"] == 0


@pytest.mark.api_test
def test_unit_test(api_client: TestClient):
    assert True
