import dectate


def test_construction(rs_registry):
    dectate.commit(rs_registry)
    # requests = rs_registry.config.requests
    # assert 0 == len(requests)

# def test_whole_damn_thing(initialized_sm):
#     services = initialized_sm.services
#     request_service = services['request']
#     assert 9 == list(initialized_sm.services.values())[0]
