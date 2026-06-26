from __future__ import annotations

from ..language.language import Language
from ..text.text_statistics import TextStatistics
from .formula import Formula
from .formula_result import FormulaResult


class Crawford(Formula):
    def name(self) -> str:
        return "crawford"

    def description(self) -> str:
        return "Crawford Formula - Spanish readability for elementary school texts."

    def supported_languages(self) -> list[str]:
        return ["es"]

    def calculate(self, stats: TextStatistics, language: Language) -> FormulaResult:
        word_count = stats.word_count if stats.word_count > 0 else 1
        sentence_count = stats.sentence_count if stats.sentence_count > 0 else 1

        average_letters = stats.letter_count / word_count
        sentences_per_100 = (sentence_count / word_count) * 100.0
        score = -0.205 * average_letters + 0.049 * sentences_per_100 - 3.407

        return FormulaResult(
            formula_name=self.name(),
            language_code=language.code,
            score=round(score, 1),
            grade_level=None,
            interpretation=self._interpret(score),
            inputs={
                "avgLettersPerWord": round(average_letters, 2),
                "sentencesPer100Words": round(sentences_per_100, 2),
            },
        )

    @staticmethod
    def _interpret(score: float) -> str:
        if score >= 9.0:
            return "Very Easy"
        elif score >= 7.0:
            return "Easy"
        elif score >= 5.0:
            return "Standard"
        elif score >= 3.0:
            return "Difficult"
        else:
            return "Very Difficult"
