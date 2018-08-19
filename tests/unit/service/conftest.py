import pytest

from kaybee_component.service.configuration import ServiceManagerConfig


@pytest.fixture
def sm_config() -> ServiceManagerConfig:
    config = ServiceManagerConfig()
    return config
