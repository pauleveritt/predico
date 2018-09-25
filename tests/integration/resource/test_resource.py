import pytest

from kaybee_component.services.request.service import RequestService
from kaybee_component.services.resource.service import ResourceService
from tests.integration.view.conftest import ForView1


@pytest.fixture
def rs(services):
    rs: ResourceService = services['resource']

    return rs


@pytest.fixture
def sample_resources(rs):
    rs.add_resource(rtype='article', id='more/about')
    rs.add_resource(rtype='article', id='more/contact')


def test_resources_empty(rs):
    assert {} == rs.resources


def test_add_get_resource(rs):
    resourceid = 'more/about'
    resource = rs.add_resource(rtype='article', id=resourceid)
    assert resourceid == resource.id
    assert resource == rs.resources[resourceid]


def test_request_resource(services, sample_resources):
    request_service: RequestService = services['request']

    # The outside world (the system) initiates the making of a
    # request, passing in the data needed for that kind of request,
    # e.g. a SphinxRequest. Perhaps a callable is passed into
    # RequestServiceConfig, or an adapter is registered.
    request = request_service.make_request(resourceid='more/about')

    # Request: Did the request get the correct one?
    assert 'more/about' == request.resource.id
