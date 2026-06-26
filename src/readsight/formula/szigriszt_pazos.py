from __future__ import annotations

from ..language.language import Language
from ..text.text_statistics import TextStatistics
from .formula import Formula
from .formula_result import FormulaResult


class SzigrisztPazos(Formula):
    def name(self) -> str:
        return "szigriszt_pazos"

    def description(self) -> str:
        return "Szigriszt-Pazos Perspicuity Index - Spanish readability formula."

    def supported_languages(self) -> list[str]:
        return ["es"]

    def calculate(self, stats: TextStatistics, language: Language) -> FormulaResult:
        word_count = stats.word_count if stats.word_count > 0 else 1
        P = stats.average_words_per_sentence  # noqa: N806

        syllables_per_word = stats.syllable_count / word_count
        syllables_per_100 = round(syllables_per_word * 100.0, 1)
        score = round(206.835 - 62.3 * syllables_per_word - P, 1)

        return FormulaResult(
            formula_name=self.name(),
            language_code=language.code,
            score=score,
            grade_level=None,
            interpretation=self._interpret(score),
            inputs={
                "syllablesPer100": syllables_per_100,
                "wordsPerSentence": round(P, 1),
            },
        )

    @staticmethod
    def _interpret(score: float) -> str:
        if score >= 85.0:
            return "Very Easy"
        elif score >= 75.0:
            return "Easy"
        elif score >= 65.0:
            return "Fairly Easy"
        elif score >= 55.0:
            return "Standard"
        elif score >= 40.0:
            return "Fairly Difficult"
        elif score >= 30.0:
            return "Difficult"
        else:
            return "Very Difficult"
