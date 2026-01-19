import allure


@allure.feature("Ingredients")
@allure.title("Получение списка ингредиентов: 200 OK + структура ответа")
def test_get_ingredients_success(client):
    r = client.get_ingredients()
    body = r.json()

    assert r.status_code == 200
    assert body.get("success") is True
    assert "data" in body
    assert isinstance(body["data"], list)
    assert len(body["data"]) > 0

    first = body["data"][0]
    assert "_id" in first
    assert "type" in first
    assert "name" in first
