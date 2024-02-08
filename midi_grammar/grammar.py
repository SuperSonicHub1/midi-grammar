"""
TODO: Add union
"""
from dataclasses import dataclass
from random import choice
from typing import Protocol, TypeVar, Generic

T = TypeVar('T')

class Node(Protocol, Generic[T]):
    def __call__(self) -> T:
        ...

@dataclass
class Terminal(Generic[T], Node[T]):
    terminal: T

    def __call__(self) -> T:
        return self.terminal

@dataclass
class Set(Generic[T], Node[T]):
    elements: set[T]

    def __call__(self) -> T:
        return choice(list(self.elements))

@dataclass
class Grammar(Generic[T]):
    symbols: list[Node[T]]

    def generate(self) -> list[T]:
        return [symbol() for symbol in self.symbols]
