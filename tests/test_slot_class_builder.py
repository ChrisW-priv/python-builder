import pytest
from python_builder.builder import add_builder


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
