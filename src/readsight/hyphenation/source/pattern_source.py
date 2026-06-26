from __future__ import annotations

from abc import ABC, abstractmethod


class PatternSource(ABC):
    @abstractmethod
    def load(self) -> dict[str, object]:
        """Returns {patterns, exceptions, maxPatternLength} dict."""
