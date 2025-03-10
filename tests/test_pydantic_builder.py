import pytest
from python_builder.builder import add_builder
from pydantic import BaseModel


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
    builder = PydanticModel.builder()
    with pytest.raises(TypeError):
        builder.set("invalid_field", "value")


def test_pydantic_builder_allowed_fields_enforcement():
    @add_builder
    class AnotherPydanticModel(BaseModel):
        foo: str

    builder = AnotherPydanticModel.builder()
    builder = builder.set("foo", "valid")
    instance = builder.build()
    assert instance.foo == "valid"

    with pytest.raises(TypeError):
        builder.set("bar", 123)


def test_pydantic_builder_disable_allowed_fields():
    @add_builder(limit_to_allowed_fields=False)
    class FlexiblePydanticModel(BaseModel):
        foo: str

    builder = FlexiblePydanticModel.builder()
    builder = builder.set("foo", "valid")
    builder = builder.set("bar", 123)
    instance = builder.build()
    assert instance.foo == "valid"
