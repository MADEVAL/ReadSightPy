from __future__ import annotations

from ..language.language import Language
from ..text.text_statistics import TextStatistics
from .formula import Formula
from .formula_result import FormulaResult


class GutierrezPolini(Formula):
    def name(self) -> str:
        return "gutierrez_polini"

    def description(self) -> str:
        return "Gutierrez de Polini Understandability Index - Spanish readability for elementary education."

    def supported_languages(self) -> list[str]:
        return ["es"]

    def calculate(self, stats: TextStatistics, language: Language) -> FormulaResult:
        word_count = stats.word_count if stats.word_count > 0 else 1
        score = 95.2 - 9.7 * (stats.letter_count / word_count) - 0.35 * stats.average_words_per_sentence

        return FormulaResult(
            formula_name=self.name(),
            language_code=language.code,
            score=round(score, 1),
            grade_level=None,
            interpretation=self._interpret(score),
            inputs={
                "lettersPerWord": round(stats.letter_count / word_count, 2),
                "wordsPerSentence": round(stats.average_words_per_sentence, 2),
            },
        )

    @staticmethod
    def _interpret(score: float) -> str:
        if score >= 80.0:
            return "Very Easy"
        elif score >= 70.0:
            return "Easy"
        elif score >= 50.0:
            return "Standard"
        elif score >= 30.0:
            return "Difficult"
        else:
            return "Very Difficult"
