import requests
import allure
import pytest
from data.config import BASE_URL, ORDERS_LIST_ENDPOINT

def create_order(payload):
    """Функция для создания заказа."""
    return requests.post(f"{BASE_URL}{ORDERS_LIST_ENDPOINT}", json=payload)

class TestCreateOrder:

    @pytest.mark.parametrize('color', [
        ['BLACK'],
        ['GREY'],
        ['BLACK', 'GREY'],
        []
    ])
    @allure.title('Создание заказа')
    @allure.description('Проверка создания заказа с разными цветами (код - 201 и наличие track в ответе)')
    def test_create_order(self, color):
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": color
        }

        response = create_order(payload)

        assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"
        assert 'track' in response.json(), "Response JSON does not contain 'track' key"
