import pytest
from httpx import AsyncClient, ASGITransport
from faker import Faker
from app.main import app
from app.main import db

@pytest.fixture(autouse=True)
def clear_db():
    db.clear()

fake = Faker()

@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
        
@pytest.mark.asyncio
async def test_custom_exception_a(client):
    response = await client.get("/check?flag=false")

    assert response.status_code == 400
    assert response.json()["error"] is not None
    
@pytest.mark.asyncio
async def test_custom_exception_b(client):
    response = await client.get("/items/999")

    assert response.status_code == 404
    
@pytest.mark.asyncio
async def test_success_case(client):
    response = await client.get("/check?flag=true")

    assert response.status_code == 200
    
@pytest.mark.asyncio
async def test_validation_error(client):
    data = {
        "username": "test",
        "age": 10, 
        "email": "not-email",
        "password": "123"
    }

    response = await client.post("/users", json=data)

    assert response.status_code == 422
    assert "details" in response.json()
    
@pytest.mark.asyncio
async def test_valid_user(client):
    data = {
        "username": fake.name(),
        "age": 25,
        "email": fake.email(),
        "password": "strongpass"
    }

    response = await client.post("/users", json=data)

    assert response.status_code == 200
    
@pytest.mark.asyncio
async def test_create_simple_user(client):
    data = {"name": fake.name()}

    response = await client.post("/simple-users", json=data)

    assert response.status_code == 201
    assert "id" in response.json()
    
@pytest.mark.asyncio
async def test_get_simple_user(client):
    create = await client.post("/simple-users", json={"name": "test"})
    user_id = create.json()["id"]

    response = await client.get(f"/simple-users/{user_id}")

    assert response.status_code == 200
    
@pytest.mark.asyncio
async def test_get_not_found(client):
    response = await client.get("/simple-users/999")

    assert response.status_code == 404
    
@pytest.mark.asyncio
async def test_delete_user(client):
    create = await client.post("/simple-users", json={"name": "test"})
    user_id = create.json()["id"]

    response = await client.delete(f"/simple-users/{user_id}")

    assert response.status_code == 204
    
@pytest.mark.asyncio
async def test_delete_twice(client):
    create = await client.post("/simple-users", json={"name": "test"})
    user_id = create.json()["id"]

    await client.delete(f"/simple-users/{user_id}")
    response = await client.delete(f"/simple-users/{user_id}")

    assert response.status_code == 404