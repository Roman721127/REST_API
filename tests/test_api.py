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
async def test_crud_lifecycle():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        create_res = await ac.post("/books", json={
            "title": "Test Book",
            "author": "Author",
            "status": "available",
            "year": 2024
        })
        book_id = create_res.json()["_id"]
        assert create_res.status_code == 201

        update_res = await ac.put(f"/books/{book_id}", json={"title": "Updated Title"})
        assert update_res.status_code == 200
        assert update_res.json()["title"] == "Updated Title"

        get_res = await ac.get(f"/books/{book_id}")
        assert get_res.status_code == 200

        del_res = await ac.delete(f"/books/{book_id}")
        assert del_res.status_code == 204

        ver_res = await ac.get(f"/books/{book_id}")
        assert ver_res.status_code == 404