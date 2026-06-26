from __future__ import annotations

from typing import Any

import regex  # type: ignore[import-untyped]

from ..language.language import Language


class TextSplitter:
    def __init__(self, language: Language) -> None:
        self._language = language
        self._letter_pattern: Any = regex.compile(language.letter_pattern)
        self._sentence_boundary_pattern: Any = regex.compile(language.sentence_boundary_pattern)
        self._word_split_pattern: Any = regex.compile(language.word_split_pattern)

    def split_words(self, text: str) -> list[str]:
        text = text.strip()
        if not text:
            return []

        parts = self._word_split_pattern.split(text)
        return [w for w in parts if w]

    def split_sentences(self, text: str) -> list[str]:
        text = text.strip()
        if not text:
            return []

        parts = self._sentence_boundary_pattern.split(text)
        return [p.strip() for p in parts if p.strip()]

    def count_letters(self, text: str) -> int:
        text = text.strip()
        if not text:
            return 0

        matches = self._letter_pattern.findall(text)
        return len(matches)

    def count_words(self, text: str) -> int:
        return len(self.split_words(text))

    def count_sentences(self, text: str) -> int:
        text = text.strip()
        if not text:
            return 0

        matches = self._sentence_boundary_pattern.findall(text)
        count = len(matches)
        return count if count > 0 else 1

    def count_long_words(self, text: str, threshold: int) -> int:
        words = self.split_words(text)
        count = 0
        for word in words:
            if self.count_letters(word) > threshold:
                count += 1
        return count
