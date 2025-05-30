import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_create_user(client: TestClient):
    response = client.post(
        "/api/v1/users/sign-up",
        json={
            "name": "Renato Rodrigues",
            "email": "renato@email.com",
            "password": "123456",
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data["email"] == "renato@email.com"
    assert data["name"] == "Renato Rodrigues"


@pytest.mark.asyncio
async def test_create_user_twice(client: TestClient):
    response = client.post(
        "/api/v1/users/sign-up",
        json={
            "name": "Renato Rodrigues",
            "email": "renato@email.com",
            "password": "123456",
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert data["email"] == "renato@email.com"
    assert data["name"] == "Renato Rodrigues"

    response = client.post(
        "/api/v1/users/sign-up",
        json={
            "name": "Renato Rodrigues",
            "email": "renato@email.com",
            "password": "123456",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_auth(client: TestClient):
    response = client.post(
        "/api/v1/users/sign-up",
        json={
            "name": "Renato Rodrigues",
            "email": "renato@email.com",
            "password": "123456",
        },
    )

    assert response.status_code == 200

    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": "renato@email.com",
            "password": "123456",
        },
        params={"args": {}, "kwargs": {}},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_unauthorized(client: TestClient):
    response = client.post(
        "/api/v1/users/sign-up",
        json={
            "name": "Renato Rodrigues",
            "email": "renato@email.com",
            "password": "123456",
        },
    )

    assert response.status_code == 200

    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": "renato@email.com",
            "password": "12345678",
        },
        params={"args": {}, "kwargs": {}},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_invalid_token(client: TestClient):
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid"},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_user_me(client: TestClient):
    response = client.post(
        "/api/v1/users/sign-up",
        json={
            "name": "Renato Rodrigues",
            "email": "renato@email.com",
            "password": "123456",
        },
    )

    assert response.status_code == 200

    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": "renato@email.com",
            "password": "123456",
        },
        params={"args": {}, "kwargs": {}},
    )

    assert response.status_code == 200

    data = response.json()
    access_token = data["access_token"]

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    data = response.json()

    assert response.status_code == 200
    assert data["email"] == "renato@email.com"


@pytest.mark.asyncio
async def test_list_users(client: TestClient):
    response = client.post(
        "/api/v1/users/sign-up",
        json={
            "name": "Renato Rodrigues",
            "email": "renato@email.com",
            "password": "123456",
        },
    )

    assert response.status_code == 200

    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": "renato@email.com",
            "password": "123456",
        },
        params={"args": {}, "kwargs": {}},
    )

    assert response.status_code == 200

    data = response.json()
    access_token = data["access_token"]

    response = client.get(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["email"] == "renato@email.com"
