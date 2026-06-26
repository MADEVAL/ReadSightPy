from __future__ import annotations

from ..language.language import Language
from ..text.text_statistics import TextStatistics
from .formula import Formula
from .formula_result import FormulaResult


class FogPL(Formula):
    def name(self) -> str:
        return "fog_pl"

    def description(self) -> str:
        return "FOG-PL - Polish adaptation of Gunning Fog Index."

    def supported_languages(self) -> list[str]:
        return ["pl"]

    def calculate(self, stats: TextStatistics, language: Language) -> FormulaResult:
        word_count = stats.word_count if stats.word_count > 0 else 1
        sentence_count = stats.sentence_count if stats.sentence_count > 0 else 1

        hard_words_pct = (stats.polysyllable_count / word_count) * 100.0
        asl = word_count / sentence_count
        score = 0.4 * (asl + hard_words_pct)

        return FormulaResult(
            formula_name=self.name(),
            language_code=language.code,
            score=round(score, 1),
            grade_level=min(max(round(score, 1), 0.0), 19.0),
            interpretation=self._interpret(score),
            inputs={
                "asl": round(asl, 2),
                "hardWordsPct": round(hard_words_pct, 2),
                "polysyllableCount": stats.polysyllable_count,
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
        else:
            return "Very Hard"
