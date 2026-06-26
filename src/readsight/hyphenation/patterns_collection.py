from __future__ import annotations

from .pattern import Pattern


class PatternsCollection:
    def __init__(self) -> None:
        self._patterns: dict[str, str] = {}
        self._max_pattern_length: int = 0

    def add(self, pattern: Pattern) -> None:
        key = "".join(pattern.chars)
        weights = "".join(str(w) for w in pattern.weights)
        self._patterns[key] = weights
        if pattern.length > self._max_pattern_length:
            self._max_pattern_length = pattern.length

    def all(self) -> dict[str, str]:
        return dict(self._patterns)

    def get_weights(self, subword: str) -> str | None:
        return self._patterns.get(subword)

    def count(self) -> int:
        return len(self._patterns)

    def max_length(self) -> int:
        return self._max_pattern_length

    def is_empty(self) -> bool:
        return not self._patterns
