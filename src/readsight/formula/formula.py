from __future__ import annotations

from typing import Protocol

from ..language.language import Language
from ..text.text_statistics import TextStatistics
from .formula_result import FormulaResult


class Formula(Protocol):
    def name(self) -> str:
        ...

    def description(self) -> str:
        ...

    def supported_languages(self) -> list[str]:
        ...

    def calculate(self, stats: TextStatistics, language: Language) -> FormulaResult:
        ...
