import requests


class StellarBurgersClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        return self.session.request(method=method, url=url, timeout=15, **kwargs)

    # ---- Ingredients ----
    def get_ingredients(self):
        return self.request("GET", "/api/ingredients")

    # ---- Orders ----
    def create_order(self, ingredients: list[str] | None = None, token: str | None = None):
        headers = {}
        if token:
            headers["Authorization"] = token

        payload = {}
        if ingredients is not None:
            payload["ingredients"] = ingredients

        return self.request("POST", "/api/orders", json=payload, headers=headers)

    def get_all_orders(self):
        return self.request("GET", "/api/orders/all")

    def get_user_orders(self, token: str | None = None):
        headers = {}
        if token:
            headers["Authorization"] = token
        return self.request("GET", "/api/orders", headers=headers)

    # ---- Auth ----
    def register(self, email: str, password: str, name: str):
        payload = {"email": email, "password": password, "name": name}
        return self.request("POST", "/api/auth/register", json=payload)

    def login(self, email: str, password: str):
        payload = {"email": email, "password": password}
        return self.request("POST", "/api/auth/login", json=payload)

    def logout(self, refresh_token: str):
        payload = {"token": refresh_token}
        return self.request("POST", "/api/auth/logout", json=payload)

    def refresh_token(self, refresh_token: str):
        payload = {"token": refresh_token}
        return self.request("POST", "/api/auth/token", json=payload)

    # ---- User ----
    def get_user(self, token: str | None = None):
        headers = {}
        if token:
            headers["Authorization"] = token
        return self.request("GET", "/api/auth/user", headers=headers)

    def update_user(self, token: str, payload: dict):
        headers = {"Authorization": token}
        return self.request("PATCH", "/api/auth/user", json=payload, headers=headers)

    def delete_user(self, token: str):
        headers = {"Authorization": token}
        return self.request("DELETE", "/api/auth/user", headers=headers)

    # ---- Password reset ----
    def password_reset(self, email: str):
        payload = {"email": email}
        return self.request("POST", "/api/password-reset", json=payload)
