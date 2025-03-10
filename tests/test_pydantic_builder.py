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
