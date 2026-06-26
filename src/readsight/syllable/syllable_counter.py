from __future__ import annotations

from abc import ABC, abstractmethod


class SyllableCounter(ABC):
    @abstractmethod
    def count_syllables(self, word: str) -> int:
        ...

    @abstractmethod
    def split_syllables(self, word: str) -> list[str]:
        ...
