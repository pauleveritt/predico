from kaybee_component.service.base_service import BaseService


def test_import():
    assert 'BaseService' == BaseService.__name__
