from dataclasses import dataclass

from python_builder import add_builder


@add_builder
@dataclass
class RegularClass:
    a: int


def test_build_from_library_import():
    i = RegularClass.builder().set("a", 42).build()
    assert i.a == 42
