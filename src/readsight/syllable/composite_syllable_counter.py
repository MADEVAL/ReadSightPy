from __future__ import annotations

from .heuristic_syllable_counter import HeuristicSyllableCounter
from .syllable_counter import SyllableCounter


class CompositeSyllableCounter(SyllableCounter):
    def __init__(self, chain: list[SyllableCounter]) -> None:
        self._chain = chain

    def count_syllables(self, word: str) -> int:
        for counter in self._chain:
            if isinstance(counter, HeuristicSyllableCounter):
                if counter.has_rules():
                    return counter.count_syllables(word)
                continue
            return counter.count_syllables(word)

        last = self._chain[-1]
        return last.count_syllables(word) if last else 1

    def split_syllables(self, word: str) -> list[str]:
        for counter in self._chain:
            if isinstance(counter, HeuristicSyllableCounter):
                if counter.has_rules():
                    return counter.split_syllables(word)
                continue
            return counter.split_syllables(word)

        last = self._chain[-1]
        return last.split_syllables(word) if last else [word]
