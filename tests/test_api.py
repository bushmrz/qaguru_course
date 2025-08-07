from http import HTTPStatus
from math import ceil

import pytest
import requests
from fastapi_pagination import response

from app.models.User import User


@pytest.fixture
def all_users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()


def test_users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK

    users = response.json()["items"]
    for user in users:
        User.model_validate(user)


def test_users_no_duplicates(users):
    users_ids = [user["id"] for user in users]
    assert len(users_ids) == len(set(users_ids))


@pytest.mark.parametrize("user_id", [1, 6, 12])
def test_user(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK

    user = response.json()
    User.model_validate(user)


@pytest.mark.parametrize("user_id", [13])
def test_user_nonexistent_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
def test_user_invalid_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("page, size", [(1, 2), (2, 6), (3, 3), (3, 5)])
def test_users_pagination(app_url, page, size):
    total = 12
    response = requests.get(f"{app_url}/api/users", params={"page": page, "size": size})

    total_pages = ceil(total / size)
    last_page = total % size
    current_items_size = last_page if page == total_pages and last_page != 0 else size

    assert response.status_code == HTTPStatus.OK

    assert response.json()["total"] == total
    assert response.json()["size"] == size
    assert response.json()["page"] == page

    assert len(response.json()["items"]) == current_items_size

    assert response.json()["pages"] == total_pages


def test_users_pagination_data_from_different_pages(app_url):
    response_first = requests.get(f"{app_url}/api/users", params={"page": 1, "size": 1})
    assert response_first.status_code == HTTPStatus.OK

    response_second = requests.get(f"{app_url}/api/users", params={"page": 2, "size": 1})
    assert response_second.status_code == HTTPStatus.OK

    assert response_first.json()["items"] != response_second.json()["items"]
