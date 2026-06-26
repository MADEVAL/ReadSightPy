from __future__ import annotations

from abc import ABC, abstractmethod

from .language import Language


class LanguageRepository(ABC):
    @abstractmethod
    def find(self, language_code: str) -> Language:
        ...

    @abstractmethod
    def list_codes(self) -> list[str]:
        ...

    @abstractmethod
    def exists(self, language_code: str) -> bool:
        ...
