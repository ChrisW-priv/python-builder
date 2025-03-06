import pytest
from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel
from python_builder.builder import add_builder, Builder

# Sample Regular Python Class
@add_builder
class RegularClass:
    a: int
    b: str
    c: bool

# Sample Regular Python Class
@add_builder
class RegularClass:
    a: int
    b: str
    c: bool

    def __init__(self):
        self.a = None
        self.b = None
        self.c = None
@add_builder
@dataclass
class DataClass:
    x: Optional[float] = None
    y: Optional[str] = None
    z: Optional[int] = None

# Sample Pydantic BaseModel
@add_builder
class PydanticModel(BaseModel):
    foo: Optional[str] = None
    bar: Optional[int] = None
    baz: Optional[bool] = None

# Sample Class with __slots__
@add_builder
class SlotClass:
    __slots__ = ['x', 'y', 'z']
    x: int
    y: str
    z: bool
def test_regular_class_builder_set_valid():
    builder = RegularClass.builder()
    builder = builder.set('a', 10)
    builder = builder.set('b', 'test')
    builder = builder.set('c', True)
    instance = builder.build()
    assert instance.a == 10
    assert instance.b == 'test'
    assert instance.c is True

def test_regular_class_builder_set_invalid():
    builder = RegularClass.builder()
    with pytest.raises(AttributeError) as excinfo:
        builder.set('d', 'invalid')
    assert "Property 'd' is not defined in RegularClass" in str(excinfo.value)

def test_regular_class_builder_merge():
    builder1 = RegularClass.builder().set('a', 1)
    builder2 = RegularClass.builder().set('b', 'abc')
    merged = builder1 | builder2
    instance = merged.build()
    assert instance.a == 1
    assert instance.b == 'abc'
    assert instance.c is None

def test_regular_class_builder_override():
    builder1 = RegularClass.builder().set('b', 'abc')
    builder2 = RegularClass.builder().set('b', 'def')
    merged = builder1 | builder2
    instance = merged.build()
    assert instance.b == 'def'

def test_regular_class_builder_different_classes():
    builder = RegularClass.builder()
    dataclass_builder = DataClass.builder()
    with pytest.raises(TypeError) as excinfo:
        _ = builder | dataclass_builder
    assert "Cannot merge builders of different classes" in str(excinfo.value)

# Tests for DataClass Builder
def test_dataclass_builder_set_valid():
    builder = DataClass.builder()
    builder = builder.set('x', 3.14)
    builder = builder.set('y', 'pi')
    builder = builder.set('z', 42)
    instance = builder.build()
    assert instance.x == 3.14
    assert instance.y == 'pi'
    assert instance.z == 42

def test_dataclass_builder_set_invalid():
    builder = DataClass.builder()
    with pytest.raises(AttributeError) as excinfo:
        builder.set('unknown', 100)
    assert "Property 'unknown' is not defined in DataClass" in str(excinfo.value)

def test_dataclass_builder_merge():
    builder1 = DataClass.builder().set('x', 1.1)
    builder2 = DataClass.builder().set('y', 'merge')
    merged = builder1 | builder2
    instance = merged.build()
    assert instance.x == 1.1
    assert instance.y == 'merge'
    assert instance.z is None

# Tests for PydanticModel Builder
def test_pydantic_builder_set_valid():
    builder = PydanticModel.builder()
    builder = builder.set('foo', 'hello')
    builder = builder.set('bar', 123)
    builder = builder.set('baz', False)
    instance = builder.build()
    assert instance.foo == 'hello'
    assert instance.bar == 123
    assert instance.baz is False

def test_pydantic_builder_set_invalid():
    builder = PydanticModel.builder()
    with pytest.raises(AttributeError) as excinfo:
        builder.set('qux', 'invalid')
    assert "Property 'qux' is not defined in PydanticModel" in str(excinfo.value)

def test_pydantic_builder_merge():
    builder1 = PydanticModel.builder().set('foo', 'foo1')
    builder2 = PydanticModel.builder().set('baz', True)
    merged = builder1 | builder2
    instance = merged.build()
    assert instance.foo == 'foo1'
    assert instance.baz is True
    assert instance.bar is None

def test_pydantic_builder_override():
    builder1 = PydanticModel.builder().set('bar', 100)
    builder2 = PydanticModel.builder().set('bar', 200)
    merged = builder1 | builder2
    instance = merged.build()
    assert instance.bar == 200

# Tests for SlotClass Builder
def test_slot_class_builder_set_valid():
    builder = SlotClass.builder()
    builder = builder.set('x', 100)
    builder = builder.set('y', 'slot test')
    builder = builder.set('z', True)
    instance = builder.build()
    assert instance.x == 100
    assert instance.y == 'slot test'
    assert instance.z is True

def test_slot_class_builder_set_invalid():
    builder = SlotClass.builder()
    with pytest.raises(AttributeError) as excinfo:
        builder.set('w', 'invalid')  # 'w' is not defined in SlotClass
    assert "Property 'w' is not defined in SlotClass" in str(excinfo.value)

def test_slot_class_builder_merge():
    builder1 = SlotClass.builder().set('x', 10)
    builder2 = SlotClass.builder().set('y', 'merged')
    merged = builder1 | builder2
    instance = merged.build()
    assert instance.x == 10
    assert instance.y == 'merged'
    assert instance.z is None  # Should be set to None by default
def test_builder_initial_values():
    initial = {'a': 5, 'b': 'initial'}
    builder = RegularClass.builder().set('a', initial['a']).set('b', initial['b'])
    instance = builder.build()
    assert instance.a == 5
    assert instance.b == 'initial'
    assert instance.c is None

def test_builder_partial_build():
    builder = RegularClass.builder().set('a', 7)
    instance = builder.build()
    assert instance.a == 7
    assert instance.b is None
    assert instance.c is None

def test_builder_none_values():
    builder = RegularClass.builder().set('a', None)
    instance = builder.build()
    assert instance.a is None
