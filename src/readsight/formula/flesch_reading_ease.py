from __future__ import annotations

from ..language.language import Language
from ..text.text_statistics import TextStatistics
from .formula import Formula
from .formula_result import FormulaResult


class FleschReadingEase(Formula):
    def name(self) -> str:
        return "flesch_reading_ease"

    def description(self) -> str:
        return (
            "Flesch Reading Ease - measures text readability on a 0-100 scale "
            "(higher = easier). Coefficients vary by language."
        )

    def supported_languages(self) -> list[str]:
        return [
            "en-us", "en-gb",
            "de-1996", "de-1901", "de-ch-1901",
            "ru", "es", "it", "fr", "nl", "pt", "tr",
        ]

    def calculate(self, stats: TextStatistics, language: Language) -> FormulaResult:
        config = language.get_formula_config(self.name()) or {}

        base = 206.835
        asl = 1.015
        asw = 84.6

        if isinstance(config.get("base"), (int, float)):
            base = float(config["base"])
        if isinstance(config.get("aslMult"), (int, float)):
            asl = float(config["aslMult"])
        if isinstance(config.get("aswMult"), (int, float)):
            asw = float(config["aswMult"])

        score = base - asl * stats.average_words_per_sentence - asw * stats.average_syllables_per_word

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
            return "Fairly Hard"
        elif score >= 30.0:
            return "Hard"
        else:
            return "Very Hard"
