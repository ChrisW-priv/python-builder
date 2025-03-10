import pytest
from python_builder.builder import add_builder
from pydantic import BaseModel, ValidationError


@add_builder
class PydanticModel(BaseModel):
    foo: str
    bar: int | None = None
    baz: bool | None = None


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
