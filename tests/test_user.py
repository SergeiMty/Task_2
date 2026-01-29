import pytest
import allure


def safe_json(response):
    """
    Сервер иногда на ошибках возвращает не JSON.
    Эта штука делает тесты устойчивыми.
    """
    try:
        return response.json()
    except Exception:
        return None


@allure.feature("User")
class TestUser:

    @allure.title("Логин пользователя: success true + токены")
    def test_login_success(self, client, registered_user):
        r = client.login(email=registered_user["email"], password=registered_user["password"])
        body = r.json()

        assert r.status_code == 200
        assert body.get("success") is True
        assert "accessToken" in body
        assert "refreshToken" in body

    @allure.title("Логин с неверным паролем -> 401 + success false + message")
    def test_login_wrong_password_returns_401(self, client, registered_user):
        r = client.login(email=registered_user["email"], password="WRONG_PASS")
        body = r.json()

        assert r.status_code == 401
        assert body.get("success") is False
        assert "message" in body

    @allure.title("Получение данных пользователя с авторизацией -> 200")
    def test_get_user_authorized(self, client, registered_user):
        r = client.get_user(token=registered_user["accessToken"])
        body = r.json()

        assert r.status_code == 200
        assert body.get("success") is True
        assert "user" in body
        assert "email" in body["user"]

    @allure.title("Получение данных пользователя без авторизации -> 401/403 + message")
    def test_get_user_unauthorized(self, client):
        r = client.get_user()
        body = safe_json(r)

        assert r.status_code in (401, 403)

        # Если JSON есть — проверяем message (как просит ревью)
        if body is not None:
            assert body.get("success") is False
            assert "message" in body
        else:
            # если вдруг сервер вернул не JSON — хотя бы не пустое тело
            assert r.text is not None and len(r.text) > 0

    @pytest.mark.parametrize("new_name", ["Sergey Updated", "QA Legend", "Burger Terminator"])
    @allure.title("Обновление имени пользователя с авторизацией -> 200 + имя обновлено")
    def test_update_user_name_authorized(self, client, registered_user, new_name):
        r = client.update_user(token=registered_user["accessToken"], payload={"name": new_name})
        body = r.json()

        assert r.status_code == 200
        assert body.get("success") is True
        assert body["user"]["name"] == new_name

    @allure.title("Обновление пользователя без авторизации -> 401/403 + message")
    def test_update_user_unauthorized_returns_401(self, client):
        r = client.update_user(payload={"name": "Hacker"})
        body = safe_json(r)

        assert r.status_code in (401, 403)

        # Требование ревью: если есть message — проверяем его
        if body is not None:
            assert body.get("success") is False
            assert "message" in body
        else:
            assert r.text is not None and len(r.text) > 0

    @allure.title("Logout пользователя -> 200 success true")
    def test_logout_success(self, client, registered_user):
        r = client.logout(registered_user["refreshToken"])
        body = r.json()

        assert r.status_code == 200
        assert body.get("success") is True

    @allure.title("Обновление accessToken по refreshToken -> 200 + новые токены")
    def test_refresh_token_success(self, client, registered_user):
        r = client.refresh_token(registered_user["refreshToken"])
        body = r.json()

        assert r.status_code == 200
        assert body.get("success") is True
        assert "accessToken" in body
        assert "refreshToken" in body

    @allure.title("Password reset: отправка письма -> 200 success true")
    def test_password_reset_success(self, client, registered_user):
        r = client.password_reset(registered_user["email"])
        body = r.json()

        assert r.status_code == 200
        assert body.get("success") is True
        assert "message" in body
