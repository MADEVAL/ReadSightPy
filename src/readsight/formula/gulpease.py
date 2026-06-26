from __future__ import annotations

from ..language.language import Language
from ..text.text_statistics import TextStatistics
from .formula import Formula
from .formula_result import FormulaResult


class Gulpease(Formula):
    def name(self) -> str:
        return "gulpease"

    def description(self) -> str:
        return "Gulpease Index - Italian readability formula. Uses letter count instead of syllables."

    def supported_languages(self) -> list[str]:
        return ["it"]

    def calculate(self, stats: TextStatistics, language: Language) -> FormulaResult:
        word_count = stats.word_count if stats.word_count > 0 else 1
        score = 89.0 + (300.0 * stats.sentence_count - 10.0 * stats.letter_count) / word_count

        return FormulaResult(
            formula_name=self.name(),
            language_code=language.code,
            score=round(score, 1),
            grade_level=None,
            interpretation=self._interpret(score),
            inputs={
                "letterCount": stats.letter_count,
                "wordCount": stats.word_count,
                "sentenceCount": stats.sentence_count,
            },
        )

    @staticmethod
    def _interpret(score: float) -> str:
        if score >= 80.0:
            return "Easy for elementary school"
        elif score >= 60.0:
            return "Easy for middle school"
        elif score >= 40.0:
            return "Easy for high school"
        else:
            return "Difficult for high school"
