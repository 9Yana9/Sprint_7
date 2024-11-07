import requests
import pytest
import allure
from data.config import BASE_URL, CREATE_COURIER_ENDPOINT, LOGIN_COURIER_ENDPOINT
from data.courier import register_new_courier_and_return_login_password

@pytest.fixture
def create_and_delete_courier():
    """Фикстура для создания курьера и удаления его после теста."""
    login_pass = register_new_courier_and_return_login_password()
    yield {
        "login": login_pass[0],
        "password": login_pass[1]
    }
    # Авторизация курьера для получения id, если успешная регистрация прошла
    response = requests.post(f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}", data={
        "login": login_pass[0],
        "password": login_pass[1]
    })
    if response.status_code == 200:
        courier_id = response.json().get("id")
        if courier_id:
            requests.delete(f"{BASE_URL}{CREATE_COURIER_ENDPOINT}/{courier_id}")

def login_courier(login, password):
    """Функция для авторизации курьера."""
    return requests.post(f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}", data={"login": login, "password": password})

class TestLoginCourier:
    @allure.title('Успешная авторизация курьера')
    @allure.description('Проверка получения ID курьера при авторизации с корректными данными')
    def test_successful_login(self, create_and_delete_courier):
        payload = create_and_delete_courier
        response = login_courier(payload["login"], payload["password"])

        assert response.status_code == 200
        assert 'id' in response.json()

    @allure.title('Авторизация с неверным паролем')
    @allure.description('Проверка ошибки при попытке авторизации с неверным паролем')
    def test_login_with_wrong_password(self, create_and_delete_courier):
        payload = {
            "login": create_and_delete_courier["login"],
            "password": "wrong_password"
        }
        response = login_courier(payload["login"], payload["password"])

        assert response.status_code == 404
        assert response.json() == {"code": 404, "message": "Учетная запись не найдена"}

    @allure.title('Авторизация без обязательного поля "password"')
    @allure.description('Проверка ошибки при попытке авторизации без пароля')
    def test_login_without_password(self, create_and_delete_courier):
        payload = {
            "login": create_and_delete_courier["login"],
            "password": ""
        }
        response = login_courier(payload["login"], payload["password"])

        assert response.status_code == 400
        assert response.json() == {"code": 400, "message": "Недостаточно данных для входа"}

