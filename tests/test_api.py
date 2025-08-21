from http import HTTPStatus
import pytest
import requests
from app.models.User import User


@pytest.mark.usefixtures("fill_test_data")
def test_users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK

    user_list = response.json()
    for user in user_list:
        User.model_validate(user)

@pytest.mark.usefixtures("fill_test_data")
def test_users_no_duplicates(users):
    users_ids = [user["id"] for user in users]
    assert len(users_ids) == len(set(users_ids))


@pytest.mark.parametrize("user_id", [130])
def test_user_nonexistent_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == "User not found"


@pytest.mark.parametrize("user_id", [-1, "fafaf"])
def test_user_invalid_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

def test_add_user(app_url):
    response = requests.post(url=f"{app_url}/api/users/",
                             json={"email":"example@mail.ma", "first_name": "John", "last_name": "Harris"})

    assert response.status_code == HTTPStatus.CREATED

def test_delete_user(app_url, create_user):
    user_id = create_user
    response = requests.delete(url=f"{app_url}/api/users/{user_id}")

    assert response.status_code == HTTPStatus.OK

def test_patch_user(app_url, create_user):
    user_id = create_user
    response = requests.patch(url=f"{app_url}/api/users/{user_id}", json={"email":"ex@maol.ew"})

    assert response.status_code == HTTPStatus.OK

    requests.delete(url=f"{app_url}/api/users/{user_id}")


def test_delete_user_negative(app_url):
    response = requests.delete(url=f"{app_url}/api/users/-1")

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()['detail'] == "Invalid user id"

def test_get_delete_user(app_url, create_user):
    user_id = create_user
    response = requests.delete(url=f"{app_url}/api/users/{user_id}")

    assert response.status_code == HTTPStatus.OK

    response = requests.get(url=f"{app_url}/api/users/{user_id}")

    assert response.status_code == HTTPStatus.NOT_FOUND

