import pytest

from kaybee_component.services.request.config import RequestServiceConfig


@pytest.fixture
def requestservice_config() -> RequestServiceConfig:
    config = RequestServiceConfig(flag=99)
    return config
