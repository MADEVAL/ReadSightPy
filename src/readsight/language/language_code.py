from __future__ import annotations


class LanguageCode:
    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:
        self._value = self._normalize(value)

    @property
    def value(self) -> str:
        return self._value

    @staticmethod
    def _normalize(code: str) -> str:
        return code.strip().lower()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LanguageCode):
            return self._value == other._value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"LanguageCode({self._value!r})"
