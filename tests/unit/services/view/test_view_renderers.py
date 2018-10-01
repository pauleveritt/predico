from dataclasses import dataclass

import pytest

from predico.services.view.renderers import StringFormatRenderer


@dataclass
class FakeView:
    name: str = 'Fake View'


@pytest.fixture
def string_format_renderer():
    template_string = '<h1>Hello {v.name}</h1>'
    view = FakeView()
    sfr = StringFormatRenderer(template_string=template_string, view=view)
    return sfr


def test_construction(string_format_renderer):
    assert '<h1>Hello {v.name}</h1>' == string_format_renderer.template_string


def test_render(string_format_renderer):
    output = string_format_renderer()
    assert '<h1>Hello Fake View</h1>' == output
