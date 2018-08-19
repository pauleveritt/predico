import pytest

from kaybee_component.services.view.config import ViewServiceConfig


@pytest.fixture
def viewservice_config() -> ViewServiceConfig:
    config = ViewServiceConfig(flag=99)
    return config
