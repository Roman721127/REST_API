import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_full_book_lifecycle(client):
    new_book = {"title": "Flask Book", "author": "Tester", "year": 2026, "status": "available"}
    post_res = client.post('/books', json=new_book)
    assert post_res.status_code == 201
    book_id = post_res.get_json()["_id"]

    get_res = client.get(f'/books/{book_id}')
    assert get_res.status_code == 200
    assert get_res.get_json()["title"] == "Flask Book"

    update_data = {"title": "Updated Book", "author": "Tester", "year": 2026, "status": "borrowed"}
    put_res = client.put(f'/books/{book_id}', json=update_data)
    assert put_res.status_code == 200

    del_res = client.delete(f'/books/{book_id}')
    assert del_res.status_code == 204

    check_del_res = client.get(f'/books/{book_id}')
    assert check_del_res.status_code == 404