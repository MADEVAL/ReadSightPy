from __future__ import annotations

from ..language.language import Language
from ..text.text_statistics import TextStatistics
from .formula import Formula
from .formula_result import FormulaResult


class FleschKincaidGradeLevel(Formula):
    def name(self) -> str:
        return "flesch_kincaid_grade_level"

    def description(self) -> str:
        return "Flesch-Kincaid Grade Level - converts Reading Ease into a U.S. school grade level."

    def supported_languages(self) -> list[str]:
        return [
            "en-us", "en-gb",
            "de-1996", "de-1901", "de-ch-1901",
            "ru", "es", "it", "fr", "nl", "pt", "tr",
        ]

    def calculate(self, stats: TextStatistics, language: Language) -> FormulaResult:
        score = 0.39 * stats.average_words_per_sentence + 11.8 * stats.average_syllables_per_word - 15.59

        return FormulaResult(
            formula_name=self.name(),
            language_code=language.code,
            score=round(score, 1),
            grade_level=min(max(round(score, 1), 0.0), 18.0),
            interpretation=self._interpret(score),
            inputs={
                "asl": stats.average_words_per_sentence,
                "asw": stats.average_syllables_per_word,
            },
        )

    @staticmethod
    def _interpret(score: float) -> str:
        if score <= 1.0:
            return "1st Grade"
        elif score <= 2.0:
            return "2nd Grade"
        elif score <= 3.0:
            return "3rd Grade"
        elif score <= 4.0:
            return "4th Grade"
        elif score <= 5.0:
            return "5th Grade"
        elif score <= 6.0:
            return "6th Grade"
        elif score <= 7.0:
            return "7th Grade"
        elif score <= 8.0:
            return "8th Grade"
        elif score <= 9.0:
            return "9th Grade"
        elif score <= 10.0:
            return "10th Grade"
        elif score <= 11.0:
            return "11th Grade"
        elif score <= 12.0:
            return "12th Grade"
        elif score <= 16.0:
            return "College"
        else:
            return "Graduate"
