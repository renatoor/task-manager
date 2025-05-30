import uuid
import pytest
import random
from datetime import datetime, timedelta
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_create_task(client: TestClient):
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

    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "New task",
            "description": "My new task",
            "due_date": str(datetime.now() + timedelta(weeks=4)),
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "New task"
    assert data["user"]["email"] == "renato@email.com"


@pytest.mark.asyncio
async def test_get_task(client: TestClient):
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

    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "New task",
            "description": "My new task",
            "due_date": str(datetime.now() + timedelta(weeks=4)),
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200

    data = response.json()
    task_id = data["id"]

    response = client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200

    get_data = response.json()

    assert data == get_data


@pytest.mark.asyncio
async def test_list_tasks(client: TestClient):
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

    weeks_due = [2, 3, 4, 5, 6]

    for i in range(0, 50):
        response = client.post(
            "/api/v1/tasks",
            json={
                "title": f"New task {i}",
                "description": "My new task {i}",
                "due_date": str(
                    datetime.now() + timedelta(weeks=random.choice(weeks_due))
                ),
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200

    response = client.get(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"args": {}, "kwargs": {}},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 10

    response = client.get(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"args": {}, "kwargs": {}, "offset": 10, "limit": 5},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 5


@pytest.mark.asyncio
async def test_update_task(client: TestClient):
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

    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "New task",
            "description": "My new task",
            "due_date": str(datetime.now() + timedelta(weeks=4)),
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200

    data = response.json()
    task_id = data["id"]

    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"completed": True},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200

    get_data = response.json()

    assert get_data["completed"]


@pytest.mark.asyncio
async def test_list_tasks_filter_due_date(client: TestClient):
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

    for i in range(0, 2):
        response = client.post(
            "/api/v1/tasks",
            json={
                "title": f"New task {i}",
                "description": "My new task {i}",
                "due_date": str(datetime.now() + timedelta(weeks=2)),
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200

    for i in range(0, 3):
        response = client.post(
            "/api/v1/tasks",
            json={
                "title": f"New task {i}",
                "description": "My new task {i}",
                "due_date": str(datetime.now() + timedelta(weeks=3)),
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200

    for i in range(0, 4):
        response = client.post(
            "/api/v1/tasks",
            json={
                "title": f"New task {i}",
                "description": "My new task {i}",
                "due_date": str(datetime.now() + timedelta(weeks=4)),
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200

    response = client.get(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {access_token}"},
        params={
            "args": {},
            "kwargs": {},
            "due_date": str(datetime.now() + timedelta(weeks=2)),
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    response = client.get(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {access_token}"},
        params={
            "args": {},
            "kwargs": {},
            "due_date": str(datetime.now() + timedelta(weeks=3)),
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5

    response = client.get(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {access_token}"},
        params={
            "args": {},
            "kwargs": {},
            "due_date": str(datetime.now() + timedelta(weeks=4)),
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 9


@pytest.mark.asyncio
async def test_list_tasks_completed(client: TestClient):
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

    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "New task",
            "description": "My new task",
            "due_date": str(datetime.now() + timedelta(weeks=4)),
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200

    data = response.json()
    task_id = data["id"]

    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"completed": True},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200

    response = client.get(
        "/api/v1/tasks",
        headers={"Authorization": f"Bearer {access_token}"},
        params={
            "args": {},
            "kwargs": {},
            "completed": True,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


@pytest.mark.asyncio
async def test_delete_task(client: TestClient):
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

    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "New task",
            "description": "My new task",
            "due_date": str(datetime.now() + timedelta(weeks=4)),
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200

    data = response.json()
    task_id = data["id"]

    response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_task_not_found(client: TestClient):
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
        f"/api/v1/tasks/{str(uuid.uuid4())}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404

    response = client.patch(
        f"/api/v1/tasks/{str(uuid.uuid4())}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={},
    )

    assert response.status_code == 404

    response = client.delete(
        f"/api/v1/tasks/{str(uuid.uuid4())}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404
