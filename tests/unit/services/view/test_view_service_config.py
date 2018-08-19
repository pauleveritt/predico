from kaybee_component.services.view.config import ViewServiceConfig


def test_import():
    assert 'ViewServiceConfig' == ViewServiceConfig.__name__


def test_construction(viewservice_config):
    assert 99 == viewservice_config.flag
