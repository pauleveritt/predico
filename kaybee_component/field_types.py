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
    """ Pass in a value of the field's type from the injectables """
    # Pass along any other args, but make sure metadata
    # has injectable
    if 'metadata' not in args:
        args['metadata'] = {}
    args['metadata']['injected'] = True
    return field(**args)


def injectedattr(type_, attr: str, **args) -> Field:
    """ Get an attribute off an injected type

     We could just do ``injected`` then pick apart the injected
     value. But that exposes a big surface area. Let's zero in
     on what we want.
     """
    if 'metadata' not in args:
        args['metadata'] = {}
    args['metadata']['injectedattr'] = dict(
        type_=type_,
        attr=attr
    )
    return field(**args)
