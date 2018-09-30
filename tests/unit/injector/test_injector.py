from dataclasses import dataclass, field

import pytest

from predico.field_types import injected
from predico.injector import inject, InvalidInjectable


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


def test_injector_injected():
    """ Create instance from data based on injectables """

    shoe = Shoe(size=66)
    props = dict()
    injectables = {Shoe.__name__: shoe}
    athlete = inject(props, injectables, Athlete)
    assert 66 == athlete.shoe.size


def test_injector_injected():
    """ Tell the injector to hand attribute of another injectable """

    @dataclass
    class InjectedAthlete:
        shoe_size: int = injected(Shoe, 'size')

    shoe = Shoe(size=88)
    props = dict()
    injectables = {Shoe.__name__: shoe}
    athlete = inject(props, injectables, InjectedAthlete)
    assert 88 == athlete.shoe_size


def test_injector_injectedattr_missing_class():
    """ Ask for a class not registered as injectable """

    class Jersey:
        pass

    @dataclass
    class InjectedAthlete:
        shoe_size: int = injected(Jersey, 'size')

    shoe = Shoe(size=88)
    props = dict()
    injectables = {Shoe.__name__: shoe}
    with pytest.raises(InvalidInjectable) as exc:
        inject(props, injectables, InjectedAthlete)
    expected = 'Invalid injected type Jersey requested from type'
    assert expected == str(exc.value)


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


def test_injector_defaultvalue():
    # Field has a default value which should be used instead of
    # injection
    default_shoesize = Shoe(size=34523)

    @dataclass
    class DefaultValueAthlete:
        shoe: Shoe = default_shoesize

    props = dict()
    injectables = dict()
    athlete = inject(props, injectables, DefaultValueAthlete)
    assert 34523 == athlete.shoe.size


def test_injector_defaultfactory():
    # Field has a default value which should be used instead of
    # injection

    @dataclass
    class DefaultValueAthlete:
        shoe: Shoe = field(default_factory=Shoe)

    props = dict()
    injectables = dict()
    athlete = inject(props, injectables, DefaultValueAthlete)
    assert 34523 == athlete.shoe.size


def test_injector_defaultfactory():
    # Field has a default value which should be used instead of
    # injection
    @dataclass
    class DefaultFactoryAthlete:
        shoe: Shoe = field(default_factory=Shoe)

    props = dict()
    injectables = dict()
    athlete = inject(props, injectables, DefaultFactoryAthlete)
    assert 77 == athlete.shoe.size


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
