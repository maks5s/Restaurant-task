import pytest
from unittest.mock import AsyncMock, Mock
from fastapi.testclient import TestClient

from app.auth.utils import create_access_token
from app.main import main_app
from app.core.schemas.restaurant import RestaurantReadSchema
from app.core.models import User
from app.core.models import db_helper


fake_user = User(id=1, username="testuser", hashed_password="hashed")

@pytest.fixture
def fake_session():
    return Mock()


@pytest.fixture(autouse=True)
def override_dependencies(monkeypatch):

    async def fake_get_current_user():
        return fake_user

    async def fake_session_getter():
        return AsyncMock()

    async def fake_create_restaurant(data, user, session):
        return RestaurantReadSchema(
            id=1,
            name=data.name,
            description=data.description
        )

    async def fake_get_restaurant_by_name(name: str, session):
        return None

    # Переоприділяємо залежності
    main_app.dependency_overrides[db_helper.session_getter] = fake_session_getter
    monkeypatch.setattr("app.auth.user.get_current_auth_user", fake_get_current_user)
    monkeypatch.setattr("app.crud.restaurant.create_restaurant", fake_create_restaurant)
    monkeypatch.setattr("app.crud.restaurant.get_restaurant_by_name", fake_get_restaurant_by_name)


def test_create_restaurant():
    client = TestClient(main_app)

    test_data = {
        "name": "Testaurant",
        "description": "Test Description"
    }

    token = create_access_token(fake_user)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/restaurants/", json=test_data, headers=headers)

    print(response.status_code)
    print(response.json())

    assert response.status_code == 200
    assert response.json()["name"] == "Testaurant"
