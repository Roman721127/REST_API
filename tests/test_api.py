import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.mark.asyncio
async def test_create_book():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/books", json={
            "title": "1984",
            "author": "George Orwell",
            "description": "Dystopian novel",
            "status": "available",
            "year": 1949
        })
    assert response.status_code == 201
    assert response.json()["title"] == "1984"

@pytest.mark.asyncio
async def test_get_books():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/books?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "next_cursor" in data
    assert isinstance(data["items"], list)