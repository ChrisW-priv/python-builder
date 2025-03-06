from functools import wraps
from typing import Any, Dict, Type, TypeVar, Generic
from dataclasses import is_dataclass, fields as dataclass_fields
from pydantic import BaseModel

T = TypeVar('T')

class Builder(Generic[T]):
    def __init__(self, cls: Type[T], initial_values: Dict[str, Any] = None):
        self._cls = cls
        self._values = initial_values.copy() if initial_values else {}

    def set(self, property_name: str, value: Any) -> 'Builder[T]':
        if not self._has_property(property_name):
            raise AttributeError(f"Property '{property_name}' is not defined in {self._cls.__name__}")
        new_values = self._values.copy()
        new_values[property_name] = value
        return Builder(self._cls, new_values)

    def __or__(self, other: 'Builder[T]') -> 'Builder[T]':
        if self._cls is not other._cls:
            raise TypeError("Cannot merge builders of different classes")
        combined_values = self._values.copy()
        for key, value in other._values.items():
            if value is not None:
                combined_values[key] = value
        return Builder(self._cls, combined_values)

    def build(self) -> T:
        return self._cls(**{k: v for k, v in self._values.items() if v is not None})

    def _has_property(self, property_name: str) -> bool:
        if is_dataclass(self._cls):
            return any(f.name == property_name for f in dataclass_fields(self._cls))
        elif issubclass(self._cls, BaseModel):
            return property_name in self._cls.__fields__
        else:
            return hasattr(self._cls, property_name)

def add_builder(cls: Type[T]) -> Type[T]:
    @classmethod
    def builder(cls_inner) -> Builder[T]:
        return Builder(cls_inner)
    
    cls.builder = builder
    return cls
