from dataclasses import dataclass

import pytest

from kaybee_component.injector import inject


@dataclass
class Shoe:
    size: int = 77


@dataclass
class Athlete:
    shoe: Shoe = Shoe()


def test_injector_props():
    """ Create instance based on data from passed-in props  """

    shoe = Shoe(size=55)
    props = dict(shoe=shoe)
    injectables = dict()
    athlete = inject(props, injectables, Athlete)
    assert 55 == athlete.shoe.size


def test_injector_injector():
    """ Create instance from data based on injectables """

    shoe = Shoe(size=66)
    props = dict()
    injectables = {Shoe.__name__: shoe}
    athlete = inject(props, injectables, Athlete)
    assert 66 == athlete.shoe.size


def test_injector_fielddefault():
    props = dict()
    injectables = dict()
    athlete = inject(props, injectables, Athlete)
    assert 77 == athlete.shoe.size


def test_injector_precedence():
    # When both props and injectable, choose props

    shoe = Shoe(size=55)
    props = dict(shoe=shoe)

    shoe = Shoe(size=66)
    injectables = {Shoe.__name__: shoe}

    athlete = inject(props, injectables, Athlete)
    assert 55 == athlete.shoe.size


def test_injector_failure():
    # Dataclass wants a value, doesn't have a default, and it
    # isn't in props or injector
    @dataclass
    class AgeAthlete:
        age: int  # Note that this field is required

    props = dict()
    injectables = dict()
    with pytest.raises(TypeError):
        inject(props, injectables, AgeAthlete)
