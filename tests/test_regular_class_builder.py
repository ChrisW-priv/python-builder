import pytest
from python_builder.builder import add_builder


@add_builder
class RegularClass:
    a: int
    b: str

    def __init__(self, a, b):
        self.a = a
        self.b = b


@add_builder
class OtherClass:
    x: float | None = None

    def __init__(self, **kwargs):
        self.x = kwargs.get("x", None)


@add_builder(limit_to_allowed_fields=False)
class FlexibleClass:
    a: int
    b: str

    def __init__(self, a, b):
        self.a = a
        self.b = b


def test_regular_class_builder_set_valid():
    builder = RegularClass.builder()
    builder = builder.set("a", 10)
    builder = builder.set("b", "test")
    instance = builder.build()
    assert instance.a == 10
    assert instance.b == "test"


def test_regular_class_builder_copy():
    builder = RegularClass.builder()
    builder1 = builder.set("a", 1)
    builder2 = builder.set("a", 2)
    with pytest.raises(KeyError):
        assert builder._values["a"]
    assert builder1._values["a"] == 1
    assert builder2._values["a"] == 2


def test_regular_class_builder_merge():
    builder1 = RegularClass.builder().set("a", 1).set("b", "abc")
    builder2 = RegularClass.builder().set("b", "def")
    merged = (builder1 | builder2).build()
    assert merged.a == 1
    assert merged.b == "def"


def test_regular_class_builder_allow_kwargs():
    builder = OtherClass.builder()
    with pytest.raises(TypeError):
        builder.set("x", 3.14)


def test_regular_class_builder_fail_on_bad_set():
    builder = RegularClass.builder()
    with pytest.raises(TypeError):
        builder.set("a", 10).set("b", "test").set("c", "extra")


def test_flexible_class_builder_set_invalid():
    builder = FlexibleClass.builder()
    builder.set("a", 10).set("b", "test").set("c", "extra")


def test_regular_class_builder_different_classes():
    builder = RegularClass.builder()
    dataclass_builder = OtherClass.builder()
    with pytest.raises(TypeError):
        _ = builder | dataclass_builder
