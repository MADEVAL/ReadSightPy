from __future__ import annotations

from ..language.language import Language
from ..text.text_statistics import TextStatistics
from .formula import Formula
from .formula_result import FormulaResult
from .text_statistics_helper import TextStatisticsHelper


class Spache(Formula):
    def name(self) -> str:
        return "spache"

    def description(self) -> str:
        return "Spache Readability Score - for primary-grade texts (K-4)."

    def supported_languages(self) -> list[str]:
        return ["en-us", "en-gb"]

    def calculate(self, stats: TextStatistics, language: Language) -> FormulaResult:
        difficult_pct = TextStatisticsHelper.estimate_difficult_percentage(stats)
        score = 0.121 * stats.average_words_per_sentence + 0.082 * difficult_pct + 0.659

        return FormulaResult(
            formula_name=self.name(),
            language_code=language.code,
            score=round(score, 1),
            grade_level=min(max(round(score, 1), 0.0), 5.0),
            interpretation=self._interpret(score),
            inputs={
                "averageWordsPerSentence": stats.average_words_per_sentence,
                "difficultWordPct": round(difficult_pct, 2),
            },
        )

    @staticmethod
    def _interpret(score: float) -> str:
        if score <= 2.0:
            return "1st Grade"
        elif score <= 2.5:
            return "2nd Grade"
        elif score <= 3.0:
            return "3rd Grade"
        elif score <= 3.5:
            return "4th Grade"
        else:
            return "Above 4th Grade"
