from typing import Any, Dict, Type, TypeVar, Generic, Protocol
from pydantic import BaseModel

T = TypeVar("T")


class Buildable(Protocol, Generic[T]):
    @classmethod
    def builder(cls) -> "Builder[T]": ...


class Builder(Generic[T]):
    def __init__(
        self,
        cls: Type[T],
        initial_values: Dict[str, Any] = None,
        allowed_fields: set = None,
    ):
        self._cls = cls
        self._values = initial_values.copy() if initial_values else {}
        self._allowed_fields = allowed_fields
        if allowed_fields is None and issubclass(self._cls, BaseModel):
            self._allowed_fields = set(self._cls.__fields__.keys())
        elif allowed_fields is None and hasattr(self._cls, "__slots__"):
            self._allowed_fields = set(self._cls.__slots__)

    def set(self, property_name: str, value: Any) -> "Builder[T]":
        assert isinstance(property_name, str), "property_name must be a string!"
        if (
            self._allowed_fields is not None
            and property_name not in self._allowed_fields
        ):
            raise TypeError(
                f'Cannot set property "{property_name}" on builder that has the "allowed_fields" enabled'
            )
        new_values = self._values.copy()
        new_values[property_name] = value
        return Builder(self._cls, new_values, self._allowed_fields)

    def __or__(self, other: "Builder[T]") -> "Builder[T]":
        if self._cls is not other._cls:
            raise TypeError("Cannot merge builders of different classes")
        combined_values = self._values.copy()
        combined_values.update(other._values)
        return Builder(self._cls, combined_values, self._allowed_fields)

    def build(self) -> T:
        return self._cls(**self._values)


def add_builder(cls: Type[T]) -> Type[Buildable[T]]:
    @classmethod
    def builder(cls_inner) -> "Builder[T]":
        return Builder(cls_inner)

    cls.builder = builder
    return cls
