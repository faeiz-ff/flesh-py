from __future__ import annotations
from typing import Dict


class Environment[T]:
    def __init__(
        self,
        symbols: Dict[str, T] | None = None,
        parent: Environment | None = None
    ):
        self.parent = parent
        self.symbols: Dict[str, T] = {} if symbols is None else symbols

    def get(self, key: str) -> T | None:
        value = self.symbols.get(key)
        if value is None and self.parent is not None:
            return self.parent.get(key)

        return value

    def set(self, key: str, value: T):
        if key in self.symbols:
            self.symbols[key] = value
        elif self.parent is not None:
            self.parent.set(key, value)

    def has(self, key: str) -> bool:
        if key in self.symbols:
            return True
        elif self.parent is not None:
            self.parent.has(key)

        return False
