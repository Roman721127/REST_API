import pytest
from httpx import AsyncClient, ASGITransport
import time

from main import app

pytestmark = pytest.mark.asyncio

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def auth_headers(client):
    username = f"tester_{int(time.time())}"
    password = "testpassword123"
    
    await client.post("/register", json={"username": username, "password": password})
    
    response = await client.post("/login", data={"username": username, "password": password})
    token = response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}

async def test_unauthorized_access(client):
    response = await client.get("/books")
    assert response.status_code == 401

async def test_full_book_lifecycle_with_auth(client, auth_headers):
    new_book = {
        "title": "Secret FastAPI Book", 
        "author": "Super Hacker", 
        "year": 2026, 
        "status": "available"
    }
    post_res = await client.post("/books", json=new_book, headers=auth_headers)
    assert post_res.status_code == 201
    
    book_data = post_res.json()
    book_id = book_data.get("_id") or book_data.get("id")

    get_res = await client.get(f"/books/{book_id}", headers=auth_headers)
    assert get_res.status_code == 200
    assert get_res.json()["title"] == "Secret FastAPI Book"

    update_data = {
        "title": "Secret FastAPI Book Updated", 
        "author": "Super Hacker", 
        "year": 2026, 
        "status": "borrowed"
    }
    put_res = await client.put(f"/books/{book_id}", json=update_data, headers=auth_headers)
    assert put_res.status_code == 200

    del_res = await client.delete(f"/books/{book_id}", headers=auth_headers)
    assert del_res.status_code == 204

    check_del_res = await client.get(f"/books/{book_id}", headers=auth_headers)
    assert check_del_res.status_code == 404