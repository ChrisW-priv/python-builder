from dataclasses import dataclass
import pytest
from python_builder.builder import add_builder


@add_builder
@dataclass(slots=True)
class SlotClass:
    x: int
    y: str
    z: bool


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
    with pytest.raises(TypeError):
        SlotClass.builder().set("w", "invalid")
