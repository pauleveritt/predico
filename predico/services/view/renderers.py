"""

Adapters to handle well-known renderers.

"""
import dataclasses
from dataclasses import dataclass

from predico.services.adapter.base_adapter import Adapter
from predico.services.view.base_view import View


@dataclass
class StringFormatRenderer(Adapter):
    view: View
    template_string: str

    def __call__(self):
        context = dataclasses.asdict(self.view)
        output = self.template_string.format(**context)
        return output
