from __future__ import annotations

from ..language.language import Language
from ..text.text_statistics import TextStatistics
from .formula import Formula
from .formula_result import FormulaResult
from .grade_level_interpretation import GradeLevelInterpretation


class ColemanLiau(Formula):
    def name(self) -> str:
        return "coleman_liau"

    def description(self) -> str:
        return "Coleman-Liau Index - character-based readability formula (no syllable counting needed)."

    def supported_languages(self) -> list[str]:
        return ["*"]

    def calculate(self, stats: TextStatistics, language: Language) -> FormulaResult:
        word_count = stats.word_count if stats.word_count > 0 else 1
        sentence_count = stats.sentence_count if stats.sentence_count > 0 else 1

        L = (stats.letter_count / word_count) * 100.0  # noqa: N806
        S = (sentence_count / word_count) * 100.0  # noqa: N806
        score = 0.0588 * L - 0.296 * S - 15.8

        return FormulaResult(
            formula_name=self.name(),
            language_code=language.code,
            score=round(score, 1),
            grade_level=min(max(round(score, 1), 0.0), 18.0),
            interpretation=GradeLevelInterpretation.for_score(score),
            inputs={
                "L": round(L, 2),
                "S": round(S, 2),
                "letterCount": stats.letter_count,
                "wordCount": stats.word_count,
                "sentenceCount": stats.sentence_count,
            },
        )
