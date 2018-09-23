"""

Use props and injectables to construct instance of a dataclass.

"""
from dataclasses import fields
from typing import Dict, Any, TypeVar, Generic

T = TypeVar('T')


def inject(
        props: Dict[str, Any],
        injectables: Dict[str, Any],
        target: Generic[T]
) -> T:
    """ Construct instance of target dataclass by providing its fields """

    # Make the args dict that we will construct dataclass with
    args = {}

    # Iterate through the target's fields
    for field in fields(target):
        # Basic rules of precedence
        # - First try in the props
        # - Then try in injectables
        # - Finally, if no field default value, dataclass will fail
        #   to construct

        field_name = field.name
        if field_name in props:
            args[field_name] = props[field_name]
        else:
            # Not in the passed-in props, let's try via injectables

            # Get the type of this field. Sucks that we have to use
            # name but I'm currently unwilling to do the dataclass
            # frozen/unsafe_hash/eq dance
            field_type = field.type.__name__

            # If we don't have this value in the injectables,
            # raise a custom exception
            injected_value = injectables.get(field_type, False)
            if injected_value:
                args[field_name] = injectables[field_type]

    return target(**args)
