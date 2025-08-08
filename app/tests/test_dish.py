import contextlib
import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient

from app.auth.utils import create_access_token
from app.main import main_app
from app.core.models import Employee, Restaurant, User


@pytest.fixture
def fake_employee():
    return Employee(id=1, restaurant_id=1, is_admin=True)


@pytest.fixture
def fake_restaurant():
    return Restaurant(id=1, name="Testaurant")


@pytest.fixture
def fake_session():
    return AsyncMock()


@pytest.fixture(autouse=True)
def override_dependencies(monkeypatch, fake_employee, fake_restaurant, fake_session):
    async def fake_get_admin_employee_for_restaurant():
        return fake_employee

    async def fake_check_restaurant_exists(restaurant_id: int, session: AsyncMock):
        return fake_restaurant

    async def fake_create_dish(data, restaurant_id, session):
        class DishMock:
            def __init__(self, data, restaurant_id):
                self.id = 123
                self.name = data.name
                self.description = data.description
                self.restaurant_id = restaurant_id
        return DishMock(data, restaurant_id)

    @contextlib.asynccontextmanager
    async def fake_session_getter():
        yield AsyncMock()

    monkeypatch.setattr("app.auth.user.get_admin_employee_for_restaurant", fake_get_admin_employee_for_restaurant)
    monkeypatch.setattr("app.crud.restaurant.check_restaurant_exists", fake_check_restaurant_exists)
    monkeypatch.setattr("app.crud.dish.create_dish", fake_create_dish)
    monkeypatch.setattr("app.core.models.db_helper.session_getter", fake_session_getter)


def test_add_dish_success():
    client = TestClient(main_app)

    payload = {
        "name": "Pizza Margherita",
        "description": "Classic Italian pizza"
    }

    fake_user = User(id=1, username="testuser", hashed_password="hashed")
    token = create_access_token(fake_user)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/restaurants/1/dishes", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["name"] == "Pizza Margherita"
    assert response.json()["description"] == "Classic Italian pizza"
    assert response.json()["id"] == 123
    assert response.json()["restaurant_id"] == 1
