import pytest
from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel, ValidationError
from python_builder.builder import add_builder


# Sample Regular Python Class
@add_builder
class RegularClass:
    a: int
    b: str
    c: bool

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


@add_builder
@dataclass
class DataClass:
    x: Optional[float] = None
    y: Optional[str] = None
    z: Optional[int] = None


# Sample Pydantic BaseModel
@add_builder
class PydanticModel(BaseModel):
    foo: str
    bar: Optional[int] = None
    baz: Optional[bool] = None


# Sample Class with __slots__
@add_builder
class SlotClass:
    __slots__ = ["x", "y", "z"]
    x: int
    y: str
    z: bool

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def test_regular_class_builder_set_valid():
    builder = RegularClass.builder()
    builder = builder.set("a", 10)
    builder = builder.set("b", "test")
    builder = builder.set("c", True)
    instance = builder.build()
    assert instance.a == 10
    assert instance.b == "test"
    assert instance.c is True


def test_regular_class_builder_set_invalid():
    builder = RegularClass.builder().set("d", "invalid")
    with pytest.raises(TypeError):
        builder.build()


def test_regular_class_builder_merge():
    builder1 = RegularClass.builder().set("a", 1)
    builder2 = RegularClass.builder().set("b", "abc")
    merged = builder1 | builder2
    with pytest.raises(TypeError):
        merged.build()


def test_regular_class_builder_override():
    builder1 = RegularClass.builder().set("b", "abc")
    builder2 = RegularClass.builder().set("b", "def")
    merged = builder1 | builder2
    with pytest.raises(TypeError):
        merged.build()


def test_regular_class_builder_different_classes():
    builder = RegularClass.builder()
    dataclass_builder = DataClass.builder()
    with pytest.raises(TypeError):
        _ = builder | dataclass_builder


# Tests for DataClass Builder
def test_dataclass_builder_set_valid():
    builder = DataClass.builder()
    builder = builder.set("x", 3.14)
    builder = builder.set("y", "pi")
    builder = builder.set("z", 42)
    instance = builder.build()
    assert instance.x == 3.14
    assert instance.y == "pi"
    assert instance.z == 42


def test_dataclass_builder_set_invalid():
    builder = DataClass.builder().set("unknown", 100)
    with pytest.raises(TypeError):
        builder.build()


def test_dataclass_builder_merge():
    builder1 = DataClass.builder().set("x", 1.1)
    builder2 = DataClass.builder().set("y", "merge")
    merged = builder1 | builder2
    instance = merged.build()
    assert instance.x == 1.1
    assert instance.y == "merge"
    assert instance.z is None


# Tests for PydanticModel Builder
def test_pydantic_builder_set_valid():
    builder = PydanticModel.builder()
    builder = builder.set("foo", "hello")
    builder = builder.set("bar", 123)
    builder = builder.set("baz", False)
    instance = builder.build()
    assert instance.foo == "hello"
    assert instance.bar == 123
    assert instance.baz is False


def test_pydantic_builder_set_invalid():
    builder = PydanticModel.builder().set("qux", "invalid")
    with pytest.raises(ValidationError):
        builder.build()


def test_pydantic_builder_merge():
    builder1 = PydanticModel.builder().set("foo", "foo1")
    builder2 = PydanticModel.builder().set("baz", True)
    merged = builder1 | builder2
    instance = merged.build()
    assert instance.foo == "foo1"
    assert instance.baz is True
    assert instance.bar is None


def test_pydantic_builder_override():
    builder1 = PydanticModel.builder().set("foo", "100")
    builder2 = PydanticModel.builder().set("foo", "200")
    merged = builder1 | builder2
    instance = merged.build()
    assert instance.foo == "200"


# Tests for SlotClass Builder
def test_slot_class_builder_set_valid():
    builder = SlotClass.builder()
    builder = builder.set("x", 100)
    builder = builder.set("y", "slot test")
    builder = builder.set("z", True)
    instance = builder.build()
    assert instance.x == 100
    assert instance.y == "slot test"
    assert instance.z is True


def test_slot_class_builder_set_invalid():
    builder = SlotClass.builder().set("w", "invalid")
    with pytest.raises(TypeError):
        builder.build()


def test_slot_class_builder_merge():
    builder1 = SlotClass.builder().set("x", 10)
    builder2 = SlotClass.builder().set("y", "merged")
    merged = builder1 | builder2
    with pytest.raises(TypeError):
        merged.build()


def test_builder_initial_values():
    initial = {"a": 5, "b": "initial"}
    builder = RegularClass.builder().set("a", initial["a"]).set("b", initial["b"])
    with pytest.raises(TypeError):
        builder.build()


def test_builder_partial_build():
    builder = RegularClass.builder().set("a", 7)
    with pytest.raises(TypeError):
        builder.build()


def test_builder_none_values():
    builder = RegularClass.builder().set("a", None)
    with pytest.raises(TypeError):
        builder.build()
