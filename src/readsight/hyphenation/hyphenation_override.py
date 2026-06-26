from __future__ import annotations


class HyphenationOverride:
    __slots__ = ("hyphenated", "word")

    def __init__(self, word: str, hyphenated: str) -> None:
        self.word = word
        self.hyphenated = hyphenated
