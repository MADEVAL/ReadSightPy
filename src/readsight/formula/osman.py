from __future__ import annotations

from ..language.language import Language
from ..text.text_statistics import TextStatistics
from .formula import Formula
from .formula_result import FormulaResult


class Osman(Formula):
    def name(self) -> str:
        return "osman"

    def description(self) -> str:
        return "OSMAN - Arabic readability formula combining Flesch and Fog adaptations."

    def supported_languages(self) -> list[str]:
        return ["ar"]

    def calculate(self, stats: TextStatistics, language: Language) -> FormulaResult:
        word_count = stats.word_count if stats.word_count > 0 else 1
        sentence_count = stats.sentence_count if stats.sentence_count > 0 else 1

        asl = word_count / sentence_count
        avg_letters = stats.letter_count / word_count
        hard_words_pct = (stats.polysyllable_count / word_count) * 100.0
        score = 200.0 - 2.0 * asl - 1.5 * avg_letters - 0.4 * hard_words_pct

        return FormulaResult(
            formula_name=self.name(),
            language_code=language.code,
            score=round(score, 1),
            grade_level=None,
            interpretation=self._interpret(score),
            inputs={
                "asl": round(asl, 2),
                "avgLetters": round(avg_letters, 2),
                "hardWordsPct": round(hard_words_pct, 2),
            },
        )

    @staticmethod
    def _interpret(score: float) -> str:
        if score >= 90.0:
            return "Very Easy"
        elif score >= 70.0:
            return "Easy"
        elif score >= 50.0:
            return "Standard"
        elif score >= 30.0:
            return "Difficult"
        else:
            return "Very Difficult"
