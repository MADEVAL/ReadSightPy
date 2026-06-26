from __future__ import annotations

from abc import ABC, abstractmethod


class Hyphenator(ABC):
    @abstractmethod
    def hyphenate(self, word: str) -> list[str]:
        """Split a word into syllable parts."""

    @abstractmethod
    def count_syllables(self, word: str) -> int:
        """Count the number of syllables in a word."""
