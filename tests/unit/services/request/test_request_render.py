"""

Test request.render() and the predicates related to rendering

"""


def test_get_templatestring_view(
        fake_templatestring_view,
        requestservice,
        resourceservice,
        fake_article1
):
    resourceservice.resources[fake_article1.id] = fake_article1
    request = requestservice.make_request('more/article1')
    assert 'Fake Template String View' == request.view.name

    # Render
    assert '<p>View Name: Fake Template String View</p>' == request.render()
