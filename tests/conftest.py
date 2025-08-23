import json
import os
from http import HTTPStatus
import pytest

from tests.fixture_sessions import base_session

from dotenv import load_dotenv
load_dotenv()

pytest_plugins = ['tests.fixture_sessions']


def pytest_addoption(parser):
    parser.addoption("--env", default="dev")


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")

# @pytest.fixture(autouse=True)
# def envs():
#     dotenv.load_dotenv()


@pytest.fixture
def app_url():
    return os.getenv("APP_URL")

@pytest.fixture
def create_user(base_session):
    response = base_session.post(url=f"/api/users/",
                             json={"email":"example@mail.mail", "first_name": "John", "last_name": "Harris"})

    assert response.status_code == HTTPStatus.CREATED

    user_id = response.json().get("id")

    return user_id


@pytest.fixture()
def fill_test_data(base_session):
    with open("tests/users.json") as f:
        test_data_users = json.load(f)
    api_users = []
    for user in test_data_users:
        response = base_session.post(f"/api/users/", json=user)
        api_users.append(response.json())

    user_ids = [user["id"] for user in api_users]

    yield user_ids

    for user_id in user_ids:
        base_session.delete(f"/api/users/{user_id}")

@pytest.fixture
def users(base_session):
    response = base_session.get(f"/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()