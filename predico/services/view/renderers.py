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
        """ The format strings get the view as ``v`` to allow
         properties and methods. """
        output = self.template_string.format(v=self.view)
        return output
