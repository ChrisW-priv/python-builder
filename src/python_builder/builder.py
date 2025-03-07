import inspect
from typing import Any, Dict, Type, TypeVar, Generic

T = TypeVar("T")


def get_init_params(cls):
    return (
        param for param in inspect.signature(cls.__init__).parameters if param != "self"
    )


class Builder(Generic[T]):
    def __init__(self, cls: Type[T], initial_values: Dict[str, Any] = None):
        self._cls = cls
        self._values = initial_values.copy() if initial_values else {}

    def set(self, property_name: str, value: Any) -> "Builder[T]":
        assert isinstance(property_name, str), "property_name must be a string!"
        new_values = self._values.copy()
        new_values[property_name] = value
        return Builder(self._cls, new_values)

    def __or__(self, other: "Builder[T]") -> "Builder[T]":
        if self._cls is not other._cls:
            raise TypeError("Cannot merge builders of different classes")
        combined_values = self._values.copy()
        combined_values.update(other._values)
        return Builder(self._cls, combined_values)

    def build(self) -> T:
        return self._cls(**{k: v for k, v in self._values.items()})


def add_builder(cls: Type[T]) -> Type[T]:
    @classmethod
    def builder(cls_inner) -> Builder[T]:
        return Builder(cls_inner)

    cls.builder = builder
    return cls
