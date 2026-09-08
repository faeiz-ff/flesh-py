from __future__ import annotations
from abc import ABC
from dataclasses import dataclass
from typing import Callable, List

from fleshpy.ast import Lambda
from fleshpy.error import FleshRuntimeError
from fleshpy.runtime.environment import Environment


@dataclass
class Value(ABC):
    ...


@dataclass
class Integer(Value):
    data: int

    def __add__(self, other: Integer | Float) -> Integer | Float:
        match other:
            case Integer(i):
                return Integer(self.data + i)
            case Float(f):
                return Float(self.data + f)

    def __mul__(self, other: Integer | Float) -> Integer | Float:
        match other:
            case Integer(i):
                return Integer(self.data * i)
            case Float(f):
                return Float(self.data * f)

    def __sub__(self, other: Integer | Float) -> Integer | Float:
        match other:
            case Integer(i):
                return Integer(self.data - i)
            case Float(f):
                return Float(self.data - f)

    def __truediv__(self, other: Integer | Float) -> Float:
        return Float(self.data / other.data)

    def __floordiv__(self, other: Integer) -> Integer:
        return Integer(self.data // other.data)

    def __int__(self):
        return self.data

    def __float__(self):
        return float(self.data)


@dataclass
class Float(Value):
    data: float

    def __add__(self, other: Float | Integer) -> Float:
        return Float(self.data + other.data)

    def __mul__(self, other: Float | Integer) -> Float:
        return Float(self.data * other.data)

    def __sub__(self, other: Float | Integer) -> Float:
        return Float(self.data - other.data)

    def __truediv__(self, other: Float | Integer) -> Float:
        return Float(self.data / other.data)

    def __floordiv__(self, other: Float) -> Float:
        return Float(self.data // other.data)

    def __int__(self):
        return int(self.data)

    def __float__(self):
        return self.data


@dataclass
class String(Value):
    data: str

    def __add__(self, other: Value) -> String:
        match other:
            case String(s):
                return String(self.data + s)
            case _:
                raise FleshRuntimeError(
                    "Cannot concatenate String with " +
                    other.__class__.__name__
                )


@dataclass
class Boolean(Value):
    data: bool


@dataclass
class Nil(Value):
    ...


@dataclass
class BuiltInFunction[T](Value):
    func: Callable[[List[T]], T]


@dataclass
class Function[T](Value):
    node: Lambda
    closure: Environment[T]
