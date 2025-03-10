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
        self._allowed_fields = (
            allowed_fields.copy() if allowed_fields is not None else None
        )

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


def add_builder(
    cls: Type[T] = None, *, limit_to_allowed_fields=True
) -> Type[Buildable[T]]:
    def decorator(cls_inner: Type[T]) -> Type[Buildable[T]]:
        allowed_fields = None
        if issubclass(cls_inner, BaseModel):
            allowed_fields = set(cls_inner.__fields__.keys())
        elif hasattr(cls_inner, "__slots__"):
            allowed_fields = set(cls_inner.__slots__)

        @classmethod
        def builder(cls_method) -> "Builder[T]":
            if limit_to_allowed_fields and allowed_fields is not None:
                return Builder(cls_method, allowed_fields=allowed_fields)
            return Builder(cls_method)

        cls_inner.builder = builder
        return cls_inner

    if cls is None:
        return decorator
    else:
        return decorator(cls)
