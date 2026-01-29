import requests


class StellarBurgersClient:
    """
    HTTP-клиент для Stellar Burgers API.
    Делает запросы через requests.Session, аккуратно добавляет Authorization,
    и позволяет вызывать методы как с токеном, так и без (для негативных тестов).
    """

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def request(self, method: str, path: str, token: str | None = None, **kwargs) -> requests.Response:
        """
        Универсальный метод запроса.
        token — строка из API (обычно accessToken вида "Bearer ..."), если None — запрос без авторизации.
        """
        url = f"{self.base_url}{path}" if path.startswith("/") else f"{self.base_url}/{path}"

        headers = kwargs.pop("headers", {}) or {}
        if token:
            headers["Authorization"] = token

        kwargs["headers"] = headers

        # Таймаут — чтобы тесты не висли бесконечно
        kwargs.setdefault("timeout", 15)

        return self.session.request(method=method, url=url, **kwargs)

    # ---------- Ingredients ----------
    def get_ingredients(self) -> requests.Response:
        return self.request("GET", "/api/ingredients")

    # ---------- Auth/User ----------
    def register(self, email: str, password: str, name: str) -> requests.Response:
        payload = {"email": email, "password": password, "name": name}
        return self.request("POST", "/api/auth/register", json=payload)

    def login(self, email: str, password: str) -> requests.Response:
        payload = {"email": email, "password": password}
        return self.request("POST", "/api/auth/login", json=payload)

    def get_user(self, token: str | None = None) -> requests.Response:
        return self.request("GET", "/api/auth/user", token=token)

    def update_user(self, payload: dict, token: str | None = None) -> requests.Response:
        """
        Важно: token необязательный — чтобы можно было тестировать "без авторизации".
        """
        return self.request("PATCH", "/api/auth/user", token=token, json=payload)

    def delete_user(self, token: str) -> requests.Response:
        return self.request("DELETE", "/api/auth/user", token=token)

    def logout(self, refresh_token: str) -> requests.Response:
        payload = {"token": refresh_token}
        return self.request("POST", "/api/auth/logout", json=payload)

    def refresh_token(self, refresh_token: str) -> requests.Response:
        payload = {"token": refresh_token}
        return self.request("POST", "/api/auth/token", json=payload)

    # ---------- Password reset ----------
    def password_reset(self, email: str) -> requests.Response:
        payload = {"email": email}
        return self.request("POST", "/api/password-reset", json=payload)

    # ---------- Orders ----------
    def create_order(self, ingredients: list, token: str | None = None) -> requests.Response:
        payload = {"ingredients": ingredients}
        return self.request("POST", "/api/orders", token=token, json=payload)

    def get_all_orders(self) -> requests.Response:
        # Лента заказов (общая)
        return self.request("GET", "/api/orders/all")

    def get_user_orders(self, token: str | None = None) -> requests.Response:
        # Заказы пользователя (нужна авторизация)
        return self.request("GET", "/api/orders", token=token)
