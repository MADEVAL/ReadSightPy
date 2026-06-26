from __future__ import annotations

from ..language.language import Language
from ..text.text_statistics import TextStatistics
from .formula import Formula
from .formula_result import FormulaResult


class GunningFog(Formula):
    def name(self) -> str:
        return "gunning_fog"

    def description(self) -> str:
        return "Gunning Fog Index - estimates years of education needed to understand text."

    def supported_languages(self) -> list[str]:
        return ["*"]

    def calculate(self, stats: TextStatistics, language: Language) -> FormulaResult:
        polysyllable_pct = (
            (stats.polysyllable_count / stats.word_count) * 100.0
            if stats.word_count > 0
            else 0.0
        )
        score = 0.4 * (stats.average_words_per_sentence + polysyllable_pct)

        return FormulaResult(
            formula_name=self.name(),
            language_code=language.code,
            score=round(score, 1),
            grade_level=min(max(round(score, 1), 0.0), 19.0),
            interpretation=self._interpret(score),
            inputs={
                "asl": stats.average_words_per_sentence,
                "polysyllablePct": polysyllable_pct,
                "polysyllableCount": stats.polysyllable_count,
                "wordCount": stats.word_count,
            },
        )

    @staticmethod
    def _interpret(score: float) -> str:
        if score < 6.0:
            return "Very Easy"
        elif score < 8.0:
            return "Easy"
        elif score < 12.0:
            return "Standard"
        elif score < 14.0:
            return "Hard"
        elif score < 17.0:
            return "Very Hard"
        else:
            return "Extremely Hard"
