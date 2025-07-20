import pytest


@pytest.mark.asyncio
async def test_create_short_url(client):
    response = await client.post(
        "/api/v1/urls/shorten", json={"target_url": "https://example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "code" in data
    assert data["target_url"].rstrip("/") == "https://example.com"


@pytest.mark.asyncio
async def test_redirect_short_url(client):
    create_response = await client.post(
        "/api/v1/urls/shorten", json={"target_url": "https://example.com"}
    )
    code = create_response.json()["code"]

    redirect_response = await client.get(f"/api/v1/urls/{code}", follow_redirects=False)
    assert redirect_response.status_code == 307
    assert redirect_response.headers["location"].rstrip("/") == "https://example.com"
