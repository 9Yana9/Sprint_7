import requests
import allure
from data.config import BASE_URL, ORDERS_LIST_ENDPOINT


def create_order(payload):
    """Функция для создания заказа."""
    return requests.post(f"{BASE_URL}{ORDERS_LIST_ENDPOINT}", json=payload)


class TestGetListOfOrders:

    @allure.title('Получение списка заказов')
    @allure.description('Получение списка заказов с проверкой наличия ключа "orders" в ответе и статус-кода 200')
    def test_get_list_of_orders(self):
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": "BLACK"
        }

        create_order(payload)

        response = requests.get(f"{BASE_URL}{ORDERS_LIST_ENDPOINT}")

        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        assert 'orders' in response.json(), "Response JSON does not contain 'orders' key"
        assert isinstance(response.json().get('orders'), list), "'orders' is not a list"
