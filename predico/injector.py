"""

Use props and injectables to construct instance of a dataclass.

Precedence
1) Use a prop if provided

2) Use a DI if type is provided and matches something in injectables

3) Use the default value if provided

4) Else, fail

"""
from dataclasses import fields
from typing import Dict, Any, TypeVar, Generic, Type, Optional

from predico.services.request.base_request import Request

T = TypeVar('T')


class InvalidInjectable(Exception):
    fmt = 'Invalid injected type {type} requested from {klass}'


def get_adapted_value(request: Request,
                      field_type: Type[Any]) -> Optional[Type[Any]]:
    if request and hasattr(request, 'adapters'):
        adapter_instance = request.adapters[field_type]

        # If the adapter has a __call__, return its result instead
        # of the adapter itself
        __call__ = hasattr(adapter_instance, '__call__')
        if __call__:
            return adapter_instance.__call__()
        else:
            return adapter_instance

    return None


def get_injected_value(field_metadata, source):
    """ First try for attr, then key, then call, else source """

    # We can have different flavors of the injected() field type:
    # injected(Breadcrumbs, attr='title')
    # injected(Breadcrumbs, key='title')
    # injected(Breadcrumbs) where Breadcrumbs.__call__ exists
    # injected(Breadcrumbs) where Breadcrumbs.__call__ does not exist

    if 'attr' in field_metadata:
        return getattr(source, field_metadata['attr'])
    elif 'key' in field_metadata:
        return source[field_metadata['key']]
    elif field_metadata['call'] is True:
        # field.metadata['injected'] should have one of attr, key, or
        # call. The first two aren't there, so call should be. See if
        # it is true and return the call.
        return source()

    # Otherwise, return the injectable/adapter, same as not having a field
    return source


def inject(
        props: Dict[str, Any],
        injectables: Dict[str, Any],
        target: Generic[T],
        request: Request = None
) -> T:
    """ Construct instance of target dataclass by providing its fields """

    # Make the args dict that we will construct dataclass with
    args = {}

    # Iterate through the target's fields
    for field in fields(target):
        # Basic rules of precedence
        # - First try in the props
        # - Then see if injected is being used
        # - Then try in injectables
        # - Finally, if no field default value, dataclass will fail
        #   to construct

        field_name = field.name
        if field_name in props:
            args[field_name] = props[field_name]
        elif field.metadata.get('injected', False):
            # This dataclass field is using the injected support

            # Get the type of injectable/adapter being requested and its
            # string name.
            injected = field.metadata['injected']
            injected_type = injected['type_']
            injected_name = injected_type.__name__

            # Let's get a source object for the injected_type. We'll first
            # try in the injectables and use that class. If not found there,
            # we'll get an adapter instance.
            source = injectables.get(injected_name, None)
            if not source:
                # Try to get from the adapter
                source = get_adapted_value(request, injected_type)

            if source:
                value = get_injected_value(injected, source)
                # attr_ = injected['attr']
                # # Raise exception if not getattr
                # value = getattr(source, attr_)
                args[field_name] = value

            # If we don't have this value in the injectables,
            # raise a custom exception
            if source is None:
                fmt = InvalidInjectable.fmt
                msg = fmt.format(
                    type=injected_name,
                    klass=target.__class__.__name__
                )
                raise InvalidInjectable(msg)

        elif getattr(field.type, '__name__', False):

            # Not in the passed-in props, let's try via injectables

            # Get the type of this field. Sucks that we have to use
            # name but I'm currently unwilling to do the dataclass
            # frozen/unsafe_hash/eq dance
            injected_name = field.type.__name__

            # First see if this is in the injectables
            injected_value = injectables.get(injected_name, False)
            if injected_value:
                args[field_name] = injectables[injected_name]
            else:
                # Maybe it is in the adapters
                adapted_value = get_adapted_value(request, field.type)
                if adapted_value:
                    args[field_name] = adapted_value

        else:
            # Need to hope there is a default value. We could consider
            # checking that later and raising a nice, custom exception.
            pass

    # Now that we have the args for the dataclass, construct it
    t = target(**args)
    return t
