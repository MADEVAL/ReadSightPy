from __future__ import annotations

import math

from ..language.language import Language
from ..text.text_statistics import TextStatistics
from .formula import Formula
from .formula_result import FormulaResult
from .grade_level_interpretation import GradeLevelInterpretation


class SmogIndex(Formula):
    def name(self) -> str:
        return "smog"

    def description(self) -> str:
        return "SMOG Index - Simple Measure of Gobbledygook. Estimates years of education needed."

    def supported_languages(self) -> list[str]:
        return ["*"]

    def calculate(self, stats: TextStatistics, language: Language) -> FormulaResult:
        sentence_count = stats.sentence_count if stats.sentence_count > 0 else 1
        score = 1.0430 * math.sqrt(stats.polysyllable_count * (30.0 / sentence_count)) + 3.1291

        return FormulaResult(
            formula_name=self.name(),
            language_code=language.code,
            score=round(score, 1),
            grade_level=min(max(round(score, 1), 0.0), 18.0),
            interpretation=GradeLevelInterpretation.for_score(score),
            inputs={
                "polysyllableCount": stats.polysyllable_count,
                "sentenceCount": stats.sentence_count,
            },
        )
