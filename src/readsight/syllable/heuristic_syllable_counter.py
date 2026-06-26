from __future__ import annotations

import re
from typing import Any

from .syllable_counter import SyllableCounter


class HeuristicSyllableCounter(SyllableCounter):
    def __init__(self, config: dict[str, Any] | None) -> None:
        self._config = config

        if config is not None:
            self._problem_words: dict[str, int] = config.get("problemWords", {})
            self._subtract_patterns: list[str] = config.get("subtractPatterns", [])
            self._add_patterns: list[str] = config.get("addPatterns", [])
            self._prefixes: dict[str, int] = config.get("prefixes", {})
            self._suffixes: dict[str, int] = config.get("suffixes", {})

            vowel_raw = config.get("vowelPattern")
            vowel_pattern: str = vowel_raw if isinstance(vowel_raw, str) else "[aeiouy]"
            self._vowel_chars = vowel_pattern.strip("[]")
        else:
            self._problem_words = {}
            self._subtract_patterns = []
            self._add_patterns = []
            self._prefixes = {}
            self._suffixes = {}
            self._vowel_chars = "aeiouy"

    def count_syllables(self, word: str) -> int:
        word = word.strip()
        if not word:
            return 0

        lower = word.lower()

        if lower in self._problem_words:
            return self._problem_words[lower]

        clean_raw = re.sub(r"[^\w]", "", lower, flags=re.UNICODE)
        if not isinstance(clean_raw, str) or not clean_raw:
            return 1

        clean = clean_raw
        affix_syllables = 0

        for prefix, syl_count in self._prefixes.items():
            if clean.startswith(prefix):
                clean = clean[len(prefix):]
                affix_syllables += syl_count

        for suffix, syl_count in self._suffixes.items():
            if clean.endswith(suffix):
                clean = clean[: -len(suffix)]
                affix_syllables += syl_count

        vowel_parts = re.split(f"[^{re.escape(self._vowel_chars)}]+", clean, flags=re.UNICODE)
        vowel_run_count = sum(1 for part in vowel_parts if part)

        count = vowel_run_count + affix_syllables

        for pattern in self._subtract_patterns:
            matches = re.findall(pattern, clean, flags=re.UNICODE)
            count -= len(matches)

        for pattern in self._add_patterns:
            matches = re.findall(pattern, clean, flags=re.UNICODE)
            count += len(matches)

        return max(count, 1)

    def has_rules(self) -> bool:
        return self._config is not None and (
            bool(self._problem_words)
            or bool(self._subtract_patterns)
            or bool(self._add_patterns)
            or bool(self._prefixes)
            or bool(self._suffixes)
        )

    def has_word(self, word: str) -> bool:
        word = word.strip()
        if not word:
            return False
        return word.lower() in self._problem_words

    def split_syllables(self, word: str) -> list[str]:
        syllable_count = self.count_syllables(word)

        if syllable_count <= 1:
            return [] if not word else [word]

        length = len(word)
        if syllable_count >= length:
            return list(word)

        part_len = length // syllable_count
        extra = length % syllable_count
        parts: list[str] = []
        pos = 0

        for i in range(syllable_count):
            cur_len = part_len + (1 if i < extra else 0)
            if pos + cur_len > length:
                cur_len = length - pos
            parts.append(word[pos : pos + cur_len])
            pos += cur_len

        return parts
