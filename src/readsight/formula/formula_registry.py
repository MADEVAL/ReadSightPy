from __future__ import annotations

from ..exceptions import UnsupportedFormulaException
from ..language.language import Language
from ..text.text_statistics import TextStatistics
from .formula import Formula
from .formula_result import FormulaResult


class FormulaRegistry:
    def __init__(self) -> None:
        self._formulas: dict[str, Formula] = {}

    def register(self, formula: Formula) -> None:
        self._formulas[formula.name()] = formula

    def has(self, name: str) -> bool:
        return name in self._formulas

    def get(self, name: str) -> Formula | None:
        return self._formulas.get(name)

    def list_names(self) -> list[str]:
        return list(self._formulas.keys())

    def list_for_language(self, language: Language) -> list[str]:
        result: list[str] = []
        for name, formula in self._formulas.items():
            langs = formula.supported_languages()
            if langs == ["*"] or language.code in langs:
                result.append(name)
        return result

    def calculate(self, name: str, language: Language, stats: TextStatistics) -> FormulaResult:
        formula = self._formulas.get(name)
        if formula is None or not self._is_supported_for_language(formula, language):
            raise UnsupportedFormulaException.for_language(name, language.code)
        return formula.calculate(stats, language)

    @staticmethod
    def _is_supported_for_language(formula: Formula, language: Language) -> bool:
        langs = formula.supported_languages()
        if langs == ["*"]:
            return True
        return language.code in langs
