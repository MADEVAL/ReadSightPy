from __future__ import annotations

from .hyphenation_override import HyphenationOverride


class HyphenationExceptionsCollection:
    def __init__(self) -> None:
        self._exceptions: dict[str, str] = {}

    def add(self, exception: HyphenationOverride) -> None:
        self._exceptions[exception.word] = exception.hyphenated

    def has(self, word: str) -> bool:
        return word in self._exceptions

    def get(self, word: str) -> str | None:
        return self._exceptions.get(word)

    def count(self) -> int:
        return len(self._exceptions)

    def is_empty(self) -> bool:
        return not self._exceptions

    def all(self) -> dict[str, str]:
        return dict(self._exceptions)
