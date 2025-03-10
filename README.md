# Python Builder

Simple implementation of a builder pattern for Python.
This library is done to be as small and simple as possible.
I wanted an easy wrapper around any class.

In my tests, I explicitly check if my library works with:

- base python `class`
- python `dataclass`
- python "slotted" class (using `__slots__`)
- pydantic `BaseModel`

But because of how simple the code is, I expect it to work with all classes.

## Usage

To use the Python Builder, decorate your classes with `@add_builder` and utilize the generated `builder()` method to construct instances fluently.

### Example with a Regular Python Class

```python
from python_builder import add_builder

@add_builder
class RegularClass:
    def __init__(self, a: int, b: str, c: bool):
        self.a = a
        self.b = b
        self.c = c

# Building an instance
builder = RegularClass.builder()
instance = (
    builder
    .set("a", 10)
    .set("b", "test")
    .set("c", True)
    .build()
)

print(instance.a)  # Output: 10
print(instance.b)  # Output: test
print(instance.c)  # Output: True
```

### Example with a Dataclass

```python
from dataclasses import dataclass
from python_builder import add_builder

@add_builder
@dataclass
class DataClass:
    x: float = None
    y: str = None
    z: int = None

# Building an instance
instance = (
    DataClass.builder()
    .set("x", 3.14)
    .set("y", "pi")
    .set("z", 42)
    .build()
)

print(instance.x)  # Output: 3.14
print(instance.y)  # Output: pi
print(instance.z)  # Output: 42
```

### Example with a Pydantic Model

```python
from pydantic import BaseModel
from python_builder import add_builder

@add_builder
class PydanticModel(BaseModel):
    foo: str
    bar: int
    baz: bool

# Building an instance
instance = (
    PydanticModel.builder()
    .set("foo", "hello")
    .set("bar", 123)
    .set("baz", False)
    .build()
)

print(instance.foo)  # Output: hello
print(instance.bar)  # Output: 123
print(instance.baz)  # Output: False
```

### Example with a Slotted Class

```python
from python_builder import add_builder

@add_builder
class SlotClass:
    __slots__ = ["x", "y", "z"]

    def __init__(self, x: int, y: str, z: bool):
        self.x = x
        self.y = y
        self.z = z

# Building an instance
instance = (
    SlotClass.builder()
    .set("x", 100)
    .set("y", "slot test")
    .set("z", True)
    .build()
)

print(instance.x)  # Output: 100
print(instance.y)  # Output: slot test
print(instance.z)  # Output: True
```

### Merging Builders

You can merge multiple builder instances using the `|` operator. The resulting builder inherits properties from both builders. In cases of conflicting properties, the values from the builder on the right take precedence.

```python
builder1 = RegularClass.builder().set("a", 1).set("b", "initial")
builder2 = RegularClass.builder().set("b", "overridden").set("c", True)
merged_builder = builder1 | builder2  # Merges builder1 and builder2; 'b' from builder2 takes precedence
instance = merged_builder.build()

print(instance.a)  # Output: 1       # Inherited from builder1
print(instance.b)  # Output: overridden  # Overridden by builder2
print(instance.c)  # Output: True    # Inherited from builder2
```

When merging builders using the `|` operator, the resulting builder combines the properties from both builders. If both builders set the same property, the value from the builder on the right side of the `|` operator overrides the one from the left.

### Handling Errors

If you set an invalid property or omit required properties, the builder will raise appropriate errors.

```python
# Setting an invalid property
builder = RegularClass.builder().set("d", "invalid")
instance = builder.build()  # Raises TypeError

# Building with missing required properties
builder = RegularClass.builder().set("a", 100)
instance = builder.build()  # Raises TypeError
```

These examples demonstrate how to utilize the Python Builder with different types of classes, handle merging of builders, and manage potential errors during the building process.

## Developement

I use `uv` so I expect you have it installed too. After cloning the repo, run:

```bash
uv sync
```

That should install all dev dependencies. After that, activate venv and run:

```bash
pre-commit install
```

That will auto format your code on each commit.
