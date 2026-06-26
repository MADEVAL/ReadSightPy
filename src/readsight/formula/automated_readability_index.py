from __future__ import annotations

from ..language.language import Language
from ..text.text_statistics import TextStatistics
from .formula import Formula
from .formula_result import FormulaResult
from .grade_level_interpretation import GradeLevelInterpretation


class AutomatedReadabilityIndex(Formula):
    def name(self) -> str:
        return "ari"

    def description(self) -> str:
        return "Automated Readability Index - character-based formula. Works for all alphabetic languages."

    def supported_languages(self) -> list[str]:
        return ["*"]

    def calculate(self, stats: TextStatistics, language: Language) -> FormulaResult:
        word_count = stats.word_count if stats.word_count > 0 else 1
        sentence_count = stats.sentence_count if stats.sentence_count > 0 else 1

        score = 4.71 * (stats.letter_count / word_count) + 0.5 * (word_count / sentence_count) - 21.43

        return FormulaResult(
            formula_name=self.name(),
            language_code=language.code,
            score=round(score, 1),
            grade_level=min(max(round(score, 1), 0.0), 18.0),
            interpretation=GradeLevelInterpretation.for_score(score),
            inputs={
                "charsPerWord": round(stats.letter_count / word_count, 2),
                "wordsPerSentence": round(word_count / sentence_count, 2),
            },
        )
