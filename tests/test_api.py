from http import HTTPStatus
import pytest
from app.models.User import User


@pytest.mark.usefixtures("fill_test_data")
def test_users(base_session):
    
    response = base_session.get(f"/api/users/")
    assert response.status_code == HTTPStatus.OK

    user_list = response.json()
    for user in user_list:
        User.model_validate(user)

@pytest.mark.usefixtures("fill_test_data")
def test_users_no_duplicates(users):
    users_ids = [user["id"] for user in users]
    assert len(users_ids) == len(set(users_ids))


@pytest.mark.parametrize("user_id", [130])
def test_user_nonexistent_values(user_id, base_session):
    response = base_session.get(f"/api/users/{user_id}")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == "User not found"


@pytest.mark.parametrize("user_id", [-1, "fafaf"])
def test_user_invalid_values(user_id, base_session):
    response = base_session.get(f"/api/users/{user_id}")

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

def test_add_user(base_session):
    response = base_session.post(url=f"/api/users/",
                             json={"email":"example@mail.ma", "first_name": "John", "last_name": "Harris"})

    assert response.status_code == HTTPStatus.CREATED

def test_delete_user(create_user, base_session):
    user_id = create_user
    response = base_session.delete(url=f"/api/users/{user_id}")

    assert response.status_code == HTTPStatus.OK

def test_patch_user(create_user, base_session):
    user_id = create_user
    response = base_session.patch(url=f"/api/users/{user_id}", json={"email":"ex@maol.ew"})

    assert response.status_code == HTTPStatus.OK

    base_session.delete(url=f"/api/users/{user_id}")


def test_delete_user_negative(base_session):
    response = base_session.delete(url=f"/api/users/-1")

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()['detail'] == "Invalid user id"

def test_get_delete_user(create_user, base_session):
    user_id = create_user
    response = base_session.delete(url=f"/api/users/{user_id}")

    assert response.status_code == HTTPStatus.OK

    response = base_session.get(url=f"/api/users/{user_id}")

    assert response.status_code == HTTPStatus.NOT_FOUND

