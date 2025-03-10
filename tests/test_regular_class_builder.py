import pytest
from python_builder.builder import add_builder


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
class OtherClass:
    x: float | None = None


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
    dataclass_builder = OtherClass.builder()
    with pytest.raises(TypeError):
        _ = builder | dataclass_builder
