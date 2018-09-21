import dectate


def test_construction(sm_registry):
    dectate.commit(sm_registry)
    s = sm_registry.config.services
    assert 0 == len(s)
