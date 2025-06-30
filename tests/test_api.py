import pytest
import httpx
import respx

from gitpulse.config import Config


@pytest.fixture
def config():
    return Config(token="test-token", api_base="https://api.github.com")
