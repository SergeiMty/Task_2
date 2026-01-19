import pytest
import allure


@allure.feature("User")
@allure.title("Логин пользователя: success true + токены")
def test_login_success(client, registered_user):
    r = client.login(email=registered_user["email"], password=registered_user["password"])
    body = r.json()

    assert r.status_code == 200
    assert body.get("success") is True
    assert "accessToken" in body
    assert "refreshToken" in body


@allure.feature("User")
@allure.title("Логин с неверным паролем -> 401 Unauthorized")
def test_login_wrong_password_returns_401(client, registered_user):
    r = client.login(email=registered_user["email"], password="WRONG_PASS")
    body = r.json()

    assert r.status_code == 401
    assert body.get("success") is False
    assert "message" in body


@allure.feature("User")
@allure.title("Получение данных пользователя с авторизацией -> 200")
def test_get_user_authorized(client, registered_user):
    r = client.get_user(token=registered_user["accessToken"])
    body = r.json()

    assert r.status_code == 200
    assert body.get("success") is True
    assert "user" in body
    assert "email" in body["user"]


@allure.feature("User")
@allure.title("Получение данных пользователя без авторизации -> 401")
def test_get_user_unauthorized(client):
    r = client.get_user()
    body = r.json()

    assert r.status_code == 401
    assert body.get("success") is False


@allure.feature("User")
@pytest.mark.parametrize("new_name", ["Sergey Updated", "QA Legend", "Burger Terminator"])
@allure.title("Обновление имени пользователя (PATCH) -> 200")
def test_update_user_name_authorized(client, registered_user, new_name):
    r = client.update_user(
        token=registered_user["accessToken"],
        payload={"name": new_name}
    )
    body = r.json()

    assert r.status_code == 200
    assert body.get("success") is True
    assert body["user"]["name"] == new_name


@allure.feature("User")
@allure.title("Обновление пользователя без авторизации -> 401")
def test_update_user_unauthorized_returns_401(client):
    r = client.update_user(token="Bearer FAKE_TOKEN", payload={"name": "Hacker"})
    # тут может быть 401 или 403 — зависит от сервера, но чаще 401
    assert r.status_code in (401, 403)


@allure.feature("User")
@allure.title("Logout пользователя -> 200 success true")
def test_logout_success(client, registered_user):
    r = client.logout(registered_user["refreshToken"])
    body = r.json()

    assert r.status_code == 200
    assert body.get("success") is True


@allure.feature("User")
@allure.title("Обновление accessToken по refreshToken -> 200 + новые токены")
def test_refresh_token_success(client, registered_user):
    r = client.refresh_token(registered_user["refreshToken"])
    body = r.json()

    assert r.status_code == 200
    assert body.get("success") is True
    assert "accessToken" in body
    assert "refreshToken" in body


@allure.feature("User")
@allure.title("Password reset: отправка письма -> 200 success true")
def test_password_reset_success(client, registered_user):
    r = client.password_reset(registered_user["email"])
    body = r.json()

    assert r.status_code == 200
    assert body.get("success") is True
    assert "message" in body
