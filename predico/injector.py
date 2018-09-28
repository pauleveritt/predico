"""

Use props and injectables to construct instance of a dataclass.

Precedence
1) Use a prop if provided

2) Use a DI if type is provided and matches something in injectables

3) Use the default value if provided

4) Else, fail

"""
from dataclasses import fields
from typing import Dict, Any, TypeVar, Generic

from predico.services.request.base_request import Request

T = TypeVar('T')


class InvalidInjectable(Exception):
    fmt = 'Invalid injectedattr type {type} requested from {klass}'


def inject(
        props: Dict[str, Any],
        injectables: Dict[str, Any],
        target: Generic[T],
        request: Request =None
) -> T:
    """ Construct instance of target dataclass by providing its fields """

    # Make the args dict that we will construct dataclass with
    args = {}

    # Iterate through the target's fields
    for field in fields(target):
        # Basic rules of precedence
        # - First try in the props
        # - Then see if injectedattr is being used
        # - Then try in injectables
        # - Finally, if no field default value, dataclass will fail
        #   to construct

        field_name = field.name
        if field_name in props:
            args[field_name] = props[field_name]
        elif field.metadata.get('injectedattr', False):
            # This dataclass field is using the injectedattr support
            injectedattr = field.metadata['injectedattr']
            field_type = injectedattr['type_'].__name__

            # If we don't have this value in the injectables,
            # raise a custom exception
            injected_value = injectables.get(field_type, False)
            if injected_value is False:
                fmt = InvalidInjectable.fmt
                msg = fmt.format(
                    type=field_type,
                    klass=target.__class__.__name__
                )
                raise InvalidInjectable(msg)

            # Add the type's attribute value to the arguments we are
            # providing to construct the dataclass
            type_ = injectables[field_type]
            attr_ = injectedattr['attr']
            value = getattr(type_, attr_)
            args[field_name] = value

        elif getattr(field.type, '__name__', False):

            # Not in the passed-in props, let's try via injectables

            # Get the type of this field. Sucks that we have to use
            # name but I'm currently unwilling to do the dataclass
            # frozen/unsafe_hash/eq dance
            field_type = field.type.__name__

            # First see if this is in the injectables
            injected_value = injectables.get(field_type, False)
            if injected_value:
                args[field_name] = injectables[field_type]
            else:
                # Maybe it is in the adapters
                if request and hasattr(request, 'adapters'):
                    adapted_value = request.adapters[field.type]
                    if adapted_value:
                        args[field_name] = adapted_value

        else:
            # Need to hope there is a default value. We could consider
            # checking that later and raising a nice, custom exception.
            pass

    # Now that we have the args for the dataclass, construct it
    t = target(**args)
    return t
