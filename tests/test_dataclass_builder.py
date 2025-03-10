from dataclasses import dataclass

import pytest
from python_builder.builder import add_builder


@add_builder
@dataclass
class DataClass:
    x: float | None = None
    y: str | None = None
    z: int | None = None


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
