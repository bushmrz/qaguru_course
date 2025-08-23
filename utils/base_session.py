import logging
from http import HTTPStatus
import curlify
import requests
from requests import Session


class BaseSession(Session):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.base_url = kwargs.get('base_url', None)

    def request(self, method, url, **kwargs):
        url = self.base_url + url

        response = super().request(method, url, **kwargs)
        logging.info(curlify.to_curl(response.request))
        return response

    def post(self, url, expected_status=HTTPStatus.CREATED, **kwargs):
        url = self.base_url + url
        response = requests.post(url=url, **kwargs)

        assert response.status_code == expected_status
        return response


    def get(self, url, expected_status=HTTPStatus.OK,  **kwargs):
        url = self.base_url + url
        response = requests.get(url=url, **kwargs)

        assert response.status_code == expected_status
        return response

    def patch(self, url, expected_status=HTTPStatus.OK, **kwargs):
        url = self.base_url + url
        response = requests.patch(url=url, **kwargs)

        assert response.status_code == expected_status
        return response

    def delete(self, url, expected_status=HTTPStatus.OK, **kwargs):
        url = self.base_url + url
        response = requests.patch(url=url, **kwargs)

        assert response.status_code == expected_status
        return response
