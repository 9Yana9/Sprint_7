import requests
import allure
import pytest
import logging
from data.config import BASE_URL, CREATE_COURIER_ENDPOINT, LOGIN_COURIER_ENDPOINT
from data.courier import generation_new_data_courier, register_new_courier_and_return_login_password

def create_courier(data):
    """Функция для создания курьера."""
    return requests.post(f"{BASE_URL}{CREATE_COURIER_ENDPOINT}", data=data)

def login_courier(login, password):
    """Функция для логина курьера."""
    return requests.post(f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}", data={"login": login, "password": password})

def delete_courier(courier_id):
    """Функция для удаления курьера."""
    return requests.delete(f"{BASE_URL}{CREATE_COURIER_ENDPOINT}/{courier_id}")

@pytest.fixture
def registered_courier_data():
    """Фикстура для создания данных зарегистрированного курьера."""
    login_pass = register_new_courier_and_return_login_password()
    return {
        "login": login_pass[0],
        "password": login_pass[1],
        "firstName": login_pass[2]
    }

class TestCreateCourier:

    @allure.title('Создание курьера')
    @allure.step('Проверка создания курьера (код - 201 и "ok": True)')
    def test_create_courier(self, registered_courier_data):
        data = generation_new_data_courier()
        data.pop("firstName")
        logging.info(f"Data for courier creation: {data}")
        print(data)

        response = create_courier(data)
        assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
        assert response.json() == {"ok": True}, "Неверное содержимое ответа."

        login_payload = {
            "login": data["login"],
            "password": data["password"]
        }
        login_response = login_courier(login_payload["login"], login_payload["password"])
        assert login_response.status_code == 200, "Login failed."

        courier_id = login_response.json().get("id")
        assert courier_id is not None, "Courier ID not found in login response."

        delete_response = delete_courier(courier_id)
        assert delete_response.status_code == 200, "Failed to delete courier."

    @allure.title('Проверка невозможности создать курьера с дублирующим логином')
    @allure.description('Проверка, что нельзя создать курьера с уже существующим логином (код - 409)')
    def test_create_courier_duplicate_login(self, registered_courier_data):
        response = create_courier(registered_courier_data)
        assert response.status_code == 409, f"Expected status code 409, got {response.status_code}"
        assert response.json() == {"code": 409, "message": "Этот логин уже используется. Попробуйте другой."}, \
            "Неверное содержимое ответа."

    @allure.title('Проверка создания курьера без обязательного поля "password"')
    @allure.description('Проверка, что нельзя создать курьера без пароля (код - 400)')
    def test_create_courier_without_password(self):
        data = generation_new_data_courier()
        payload = {
            "login": data["login"],
            "firstName": data["firstName"]
        }

        response = create_courier(payload)
        assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"
        assert response.json() == {"code": 400, "message": "Недостаточно данных для создания учетной записи"}, \
            "Неверное содержимое ответа."
