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

    def post(self, url, **kwargs):
        url = self.base_url + url
        response = requests.post(url=url, **kwargs)

        return response


    def get(self, url,  **kwargs):
        url = self.base_url + url
        response = requests.get(url=url, **kwargs)

        return response

    def patch(self, url, **kwargs):
        url = self.base_url + url
        response = requests.patch(url=url, **kwargs)

        return response

    def delete(self, url, **kwargs):
        url = self.base_url + url
        response = requests.delete(url=url, **kwargs)

        return response
