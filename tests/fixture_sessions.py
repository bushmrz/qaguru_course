import pytest

from utils.base_session import BaseSession
from config import Server


@pytest.fixture(scope='session')
def base_session(env):
    with BaseSession(base_url=Server(env).user_service) as session:
        yield session