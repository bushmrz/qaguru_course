import json
import os
from http import HTTPStatus

import dotenv
import pytest
import requests


@pytest.fixture(autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture
def app_url():
    return os.getenv("APP_URL")

@pytest.fixture
def create_user(app_url):
    response = requests.post(url=f"{app_url}/api/users/",
                             json={"email":"example@mail.mail", "first_name": "John", "last_name": "Harris"})

    assert response.status_code == HTTPStatus.CREATED

    user_id = response.json().get("id")

    return user_id


@pytest.fixture()
def fill_test_data(app_url):
    with open("tests/users.json") as f:
        test_data_users = json.load(f)
    api_users = []
    for user in test_data_users:
        response = requests.post(f"{app_url}/api/users/", json=user)
        api_users.append(response.json())

    user_ids = [user["id"] for user in api_users]

    yield user_ids

    for user_id in user_ids:
        requests.delete(f"{app_url}/api/users/{user_id}")

@pytest.fixture
def users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()