from __future__ import annotations

from .hyphenation_exceptions_collection import HyphenationExceptionsCollection
from .hyphenator import Hyphenator
from .patterns_collection import PatternsCollection


class LiangHyphenator(Hyphenator):
    def __init__(
        self,
        patterns: PatternsCollection,
        exceptions: HyphenationExceptionsCollection,
        min_hyphen_left: int = 2,
        min_hyphen_right: int = 2,
    ) -> None:
        self._patterns = patterns
        self._exceptions = exceptions
        self._min_hyphen_left = min_hyphen_left
        self._min_hyphen_right = min_hyphen_right
        self._user_hyphenations: dict[str, str] = {}

    def add_hyphenations(self, hyphenations: dict[str, str]) -> None:
        for word, hyphenated in hyphenations.items():
            self._user_hyphenations[word.lower()] = hyphenated.lower()

    def hyphenate(self, word: str) -> list[str]:
        word_length = len(word)

        if word_length == 0:
            return []

        if word_length < self._min_hyphen_left + self._min_hyphen_right:
            return [word]

        word_lower = word.lower()

        if word_lower in self._user_hyphenations:
            return self._split_by_hyphenation(self._user_hyphenations[word_lower], word)

        if self._exceptions.has(word_lower):
            hyphenated = self._exceptions.get(word_lower)
            if hyphenated is not None:
                return self._split_by_hyphenation(hyphenated, word)

        return self._split_by_patterns(word, word_length, word_lower)

    def count_syllables(self, word: str) -> int:
        parts = self.hyphenate(word)
        return len(parts) if parts else 0

    def _split_by_hyphenation(self, hyphenated: str, original_word: str) -> list[str]:
        parts: list[str] = []
        part = ""
        j = 0
        hyphenated_length = len(hyphenated)

        for i in range(hyphenated_length):
            char = hyphenated[i]
            if char == "-":
                if part:
                    parts.append(part)
                part = ""
            else:
                if j < len(original_word):
                    part += original_word[j]
                j += 1

        if part:
            parts.append(part)

        return parts

    def _split_by_patterns(self, word: str, word_length: int, word_lower: str) -> list[str]:
        text = "." + word_lower + "."
        text_length = word_length + 2
        pattern_length = self._patterns.max_length()

        if pattern_length > text_length:
            pattern_length = text_length

        scores: dict[int, int] = {}

        end = text_length - self._min_hyphen_right
        for start in range(end):
            max_len = min(pattern_length, text_length - start)

            for length in range(1, max_len + 1):
                subword = text[start : start + length]
                weights = self._patterns.get_weights(subword)

                if weights is None:
                    continue

                weights_length = len(weights)
                for offset in range(weights_length):
                    idx = start + offset
                    if idx >= text_length:
                        continue
                    score = int(weights[offset])
                    if idx not in scores or score > scores[idx]:
                        scores[idx] = score

        parts: list[str] = []
        part = word[: self._min_hyphen_left]
        break_end = text_length - self._min_hyphen_right

        i = self._min_hyphen_left + 1
        while i < break_end:
            if scores.get(i, 0) & 1:
                parts.append(part)
                part = ""
            if i - 1 < len(word):
                part += word[i - 1]
            i += 1

        while i < text_length - 1:
            if i - 1 < len(word):
                part += word[i - 1]
            i += 1

        if part:
            parts.append(part)

        return parts
