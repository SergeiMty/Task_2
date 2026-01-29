import uuid
import pytest

from api.client import StellarBurgersClient
from api.endpoints import BASE_URL


@pytest.fixture(scope="session")
def client():
    return StellarBurgersClient(BASE_URL)


@pytest.fixture
def user_payload():
    unique = uuid.uuid4().hex[:10]
    return {
        "email": f"sergey_{unique}@yandex.ru",
        "password": "Password123!",
        "name": "Sergey QA"
    }


@pytest.fixture
def registered_user(client, user_payload):
    """
    Регистрируем пользователя -> отдаём accessToken/refreshToken -> после теста удаляем.
    """
    r = client.register(
        email=user_payload["email"],
        password=user_payload["password"],
        name=user_payload["name"]
    )
    data = r.json()

    assert r.status_code == 200, f"Register failed: {r.status_code}, body={r.text}"
    assert data.get("success") is True, f"Register failed: body={data}"

    access_token = data["accessToken"]
    refresh_token = data["refreshToken"]

    user_data = {
        **user_payload,
        "accessToken": access_token,
        "refreshToken": refresh_token
    }

    try:
        yield user_data
    finally:
        # удаляем юзера (если токен валиден)
        try:
            client.delete_user(access_token)
        except Exception:
            pass
