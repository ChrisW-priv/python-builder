from dataclasses import dataclass

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
