from __future__ import annotations

from ..language.language import Language
from ..text.text_statistics import TextStatistics
from .formula import Formula
from .formula_result import FormulaResult


class Lix(Formula):
    def name(self) -> str:
        return "lix"

    def description(self) -> str:
        return "LIX (Läsbarhetsindex) - Scandinavian readability formula. Language-independent, uses letter count."

    def supported_languages(self) -> list[str]:
        return ["*"]

    def calculate(self, stats: TextStatistics, language: Language) -> FormulaResult:
        config = language.get_formula_config(self.name())
        threshold = 6
        if config is not None and isinstance(config, dict):
            t = config.get("longWordThreshold")
            if isinstance(t, (int, float)):
                threshold = int(t)

        long_word_pct = (
            (stats.long_word_count / stats.word_count) * 100.0
            if stats.word_count > 0
            else 0.0
        )
        score = stats.average_words_per_sentence + long_word_pct

        return FormulaResult(
            formula_name=self.name(),
            language_code=language.code,
            score=round(score, 2),
            grade_level=None,
            interpretation=self._interpret(score),
            inputs={
                "asl": stats.average_words_per_sentence,
                "longWordPct": round(long_word_pct, 2),
                "threshold": threshold,
                "longWordCount": stats.long_word_count,
                "wordCount": stats.word_count,
            },
        )

    @staticmethod
    def _interpret(score: float) -> str:
        if score < 25.0:
            return "Children's Books"
        elif score < 30.0:
            return "Simple Texts"
        elif score < 40.0:
            return "Normal / Fiction"
        elif score < 50.0:
            return "Factual Information"
        elif score < 60.0:
            return "Specialized Texts"
        else:
            return "Research / Advanced"
