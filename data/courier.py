import requests
import random
import string
from data.config import BASE_URL, CREATE_COURIER_ENDPOINT


def generation_new_data_courier():
    """Генерирует данные для нового курьера."""
    letters = string.ascii_lowercase
    return {
        "login": ''.join(random.choice(letters) for _ in range(10)),
        "password": ''.join(random.choice(letters) for _ in range(10)),
        "firstName": ''.join(random.choice(letters) for _ in range(10))
    }


def register_new_courier_and_return_login_password():
    """Регистрирует нового курьера и возвращает его логин, пароль и имя."""
    login_pass = []
    data = generation_new_data_courier()

    response = requests.post(f"{BASE_URL}{CREATE_COURIER_ENDPOINT}", data=data)

    if response.status_code == 201:
        login_pass.extend([data["login"], data["password"], data["firstName"]])

    return login_pass
