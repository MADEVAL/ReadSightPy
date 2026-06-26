from __future__ import annotations

from ..hyphenation.hyphenator import Hyphenator
from .syllable_counter import SyllableCounter


class TexSyllableCounter(SyllableCounter):
    def __init__(self, hyphenator: Hyphenator) -> None:
        self._hyphenator = hyphenator

    def count_syllables(self, word: str) -> int:
        return self._hyphenator.count_syllables(word)

    def split_syllables(self, word: str) -> list[str]:
        return self._hyphenator.hyphenate(word)
