"""

Dataclass field helpers.

It sucks to type:

.. code-block:: python

    sm_config: ServiceManagerConfig = field(
        metadata=dict(
            injected=True
        )
    )

These are some subclasses of field which wire up the common
cases.

"""
from dataclasses import field, Field


def injected(**args) -> Field:
    # Pass along any other args, but make sure metadata
    # has injectable
    if 'metadata' not in args:
        args['metadata'] = {}
    args['metadata']['injected'] = True
    return field(**args)