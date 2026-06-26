from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TextStatistics:
    letter_count: int
    word_count: int
    sentence_count: int
    syllable_count: int
    polysyllable_count: int
    average_syllables_per_word: float
    average_words_per_sentence: float
    long_word_count: int
    syllable_histogram: dict[int, int]
