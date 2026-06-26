from __future__ import annotations

from ..language.language import Language
from ..text.text_statistics import TextStatistics
from .formula import Formula
from .formula_result import FormulaResult
from .text_statistics_helper import TextStatisticsHelper


class DaleChall(Formula):
    def name(self) -> str:
        return "dale_chall"

    def description(self) -> str:
        return "Dale-Chall Readability Score - estimates difficult words via syllable heuristic (1-syllable = easy)."

    def supported_languages(self) -> list[str]:
        return ["en-us", "en-gb"]

    def calculate(self, stats: TextStatistics, language: Language) -> FormulaResult:
        difficult_pct = TextStatisticsHelper.estimate_difficult_percentage(stats)
        raw_score = 0.1579 * difficult_pct + 0.0496 * stats.average_words_per_sentence
        adjusted = raw_score + 3.6365 if difficult_pct > 5.0 else raw_score

        return FormulaResult(
            formula_name=self.name(),
            language_code=language.code,
            score=round(adjusted, 1),
            grade_level=None,
            interpretation=self._interpret(adjusted),
            inputs={
                "difficultWordPct": round(difficult_pct, 1),
                "rawScore": round(raw_score, 4),
                "averageWordsPerSentence": stats.average_words_per_sentence,
            },
        )

    @staticmethod
    def _interpret(score: float) -> str:
        if score <= 4.9:
            return "4th grade or below"
        elif score <= 5.9:
            return "5th-6th grade"
        elif score <= 6.9:
            return "7th-8th grade"
        elif score <= 7.9:
            return "9th-10th grade"
        elif score <= 8.9:
            return "11th-12th grade"
        elif score <= 9.9:
            return "College"
        else:
            return "Graduate"
