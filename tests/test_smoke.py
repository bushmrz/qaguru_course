from http import HTTPStatus

import requests
from app.models.AppStatus import AppStatus

def test_check_app_status(app_url):
    response = requests.get(f"{app_url}/status")

    assert response.status_code == HTTPStatus.OK

    response_body = response.json()
    AppStatus.model_validate(response_body)

    assert response_body["users"] == True