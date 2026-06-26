from __future__ import annotations

from abc import ABC, abstractmethod


class PatternCache(ABC):
    @abstractmethod
    def has(self, language_code: str) -> bool:
        ...

    @abstractmethod
    def get(self, language_code: str) -> dict[str, object] | None:
        """Returns pattern data dict or None"""

    @abstractmethod
    def set(self, language_code: str, data: dict[str, object]) -> None:
        ...

    @abstractmethod
    def clear(self, language_code: str) -> None:
        ...

    @abstractmethod
    def clear_all(self) -> None:
        ...
