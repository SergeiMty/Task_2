import pytest
import allure


@allure.feature("Orders")
@allure.title("Создание заказа: валидные ингредиенты -> success true")
def test_create_order_success(client):
    # сначала получаем реальные ингредиенты
    ingredients = client.get_ingredients().json()["data"]
    ingredient_ids = [ingredients[0]["_id"], ingredients[1]["_id"]]

    r = client.create_order(ingredients=ingredient_ids)
    body = r.json()

    assert r.status_code == 200
    assert body.get("success") is True
    assert "order" in body
    assert "number" in body["order"]


@allure.feature("Orders")
@allure.title("Создание заказа без ингредиентов -> 400 Bad Request")
def test_create_order_without_ingredients_returns_400(client):
    r = client.create_order(ingredients=[])
    body = r.json()

    assert r.status_code == 400
    assert body.get("success") is False
    assert "message" in body


@allure.feature("Orders")
@allure.title("Создание заказа с невалидным id ингредиента -> 500 Internal Server Error")
def test_create_order_with_invalid_ingredient_hash_returns_500(client):
    r = client.create_order(ingredients=["invalid_hash_123"])
    assert r.status_code == 500


@allure.feature("Orders")
@allure.title("Получение всех заказов -> 200 + success true + поля total/totalToday")
def test_get_all_orders(client):
    r = client.get_all_orders()
    body = r.json()

    assert r.status_code == 200
    assert body.get("success") is True
    assert "orders" in body
    assert "total" in body
    assert "totalToday" in body


@allure.feature("Orders")
@allure.title("Получение заказов пользователя без авторизации -> 401")
def test_get_user_orders_unauthorized_returns_401(client):
    r = client.get_user_orders()
    body = r.json()

    assert r.status_code == 401
    assert body.get("success") is False


@allure.feature("Orders")
@allure.title("Получение заказов пользователя с авторизацией -> 200")
def test_get_user_orders_authorized(client, registered_user):
    r = client.get_user_orders(token=registered_user["accessToken"])
    body = r.json()

    assert r.status_code == 200
    assert body.get("success") is True
    assert "orders" in body
