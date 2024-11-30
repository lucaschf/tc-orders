import dataclasses
from dataclasses import dataclass, is_dataclass

import pytest

from src.domain.__shared.value_object import ValueObject


@dataclass(frozen=True, slots=True)
class Stub(ValueObject):
    def _validate(self) -> None:
        assert self.prop is not None

    prop: str


@dataclass(frozen=True, slots=True)
class StubWithTwoProps(ValueObject):
    prop1: str
    prop2: int

    def _validate(self) -> None:
        assert self.prop1 is not None
        assert self.prop2 is not None


def test_is_a_dataclass() -> None:
    assert is_dataclass(ValueObject)


def test_value_object_immutable() -> None:
    obj = Stub(prop="prop")
    with pytest.raises(dataclasses.FrozenInstanceError):
        # noinspection PyDataclass
        obj.prop = "20"


def test_init_properties() -> None:
    prop = "prop"
    stub = Stub(prop=prop)

    assert stub.prop == prop

    prop1 = "prop1"
    prop2 = 1
    stub = StubWithTwoProps(prop1=prop1, prop2=prop2)

    assert stub.prop1 == prop1
    assert stub.prop2 == prop2


def test_convert_to_string() -> None:
    prop = "prop"
    stub = Stub(prop=prop)
    assert str(stub) == prop

    prop1 = "prop1"
    prop2 = 1
    stub = StubWithTwoProps(prop1=prop1, prop2=prop2)

    assert str(stub) == f'{{"prop1": "{prop1}", "prop2": {prop2}}}'
