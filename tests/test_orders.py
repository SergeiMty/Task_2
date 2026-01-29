import allure


@allure.feature("Orders")
class TestOrders:

    @allure.title("Создание заказа: валидные ингредиенты -> 200 + success true")
    def test_create_order_success(self, client):
        ingredients = client.get_ingredients().json()["data"]
        ingredient_ids = [ingredients[0]["_id"], ingredients[1]["_id"]]

        r = client.create_order(ingredients=ingredient_ids)
        body = r.json()

        assert r.status_code == 200
        assert body.get("success") is True
        assert "order" in body
        assert "number" in body["order"]

    @allure.title("Создание заказа без ингредиентов -> 400 + success false + message")
    def test_create_order_without_ingredients_returns_400(self, client):
        r = client.create_order(ingredients=[])
        body = r.json()

        assert r.status_code == 400
        assert body.get("success") is False
        assert "message" in body

    @allure.title("Создание заказа с невалидным id ингредиента -> 500 (сервер может вернуть HTML)")
    def test_create_order_with_invalid_ingredient_hash_returns_500(self, client):
        r = client.create_order(ingredients=["invalid_hash_123"])

        # На стенде это реально 500
        assert r.status_code == 500

        # И часто это НЕ JSON, а HTML — поэтому НЕ делаем r.json()
        assert r.text is not None
        assert "Internal Server Error" in r.text

    @allure.title("Получение всех заказов -> 200 + success true + поля orders/total/totalToday")
    def test_get_all_orders(self, client):
        r = client.get_all_orders()
        body = r.json()

        assert r.status_code == 200
        assert body.get("success") is True
        assert "orders" in body
        assert "total" in body
        assert "totalToday" in body
