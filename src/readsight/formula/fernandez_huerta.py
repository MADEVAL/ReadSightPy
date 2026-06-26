from __future__ import annotations

from ..language.language import Language
from ..text.text_statistics import TextStatistics
from .formula import Formula
from .formula_result import FormulaResult


class FernandezHuerta(Formula):
    def name(self) -> str:
        return "fernandez_huerta"

    def description(self) -> str:
        return "Fernandez-Huerta - Spanish adaptation of Flesch Reading Ease."

    def supported_languages(self) -> list[str]:
        return ["es"]

    def calculate(self, stats: TextStatistics, language: Language) -> FormulaResult:
        score = 206.84 - 1.02 * stats.average_words_per_sentence - 60.0 * stats.average_syllables_per_word

        return FormulaResult(
            formula_name=self.name(),
            language_code=language.code,
            score=round(score, 1),
            grade_level=None,
            interpretation=self._interpret(score),
            inputs={
                "asl": stats.average_words_per_sentence,
                "asw": stats.average_syllables_per_word,
            },
        )

    @staticmethod
    def _interpret(score: float) -> str:
        if score >= 90.0:
            return "Very Easy"
        elif score >= 80.0:
            return "Easy"
        elif score >= 70.0:
            return "Fairly Easy"
        elif score >= 60.0:
            return "Standard"
        elif score >= 50.0:
            return "Fairly Difficult"
        elif score >= 30.0:
            return "Difficult"
        else:
            return "Very Difficult"
