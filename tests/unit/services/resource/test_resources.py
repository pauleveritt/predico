import pytest

from predico.services.resource.base_resource import Resources


@pytest.fixture
def fake_resources():
    resources = Resources()
    return resources


def test_construction(fake_resources):
    assert {} == fake_resources


def test_dict_operations(fake_resources):
    assert [] == list(fake_resources.keys())
    fake_resources['a'] = 'A'
    assert ['a'] == list(fake_resources.keys())
    a = fake_resources['a']
    assert 'A' == a
    del fake_resources['a']
    assert [] == list(fake_resources.keys())
