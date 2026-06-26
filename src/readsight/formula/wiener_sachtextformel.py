from __future__ import annotations

from typing import TypedDict

from ..language.language import Language
from ..text.text_statistics import TextStatistics
from .formula import Formula
from .formula_result import FormulaResult


class _ComputeResult(TypedDict):
    score: float
    gradeLevel: float
    inputs: dict[str, float | int]


class WienerSachtextformel(Formula):
    def name(self) -> str:
        return "wiener_sachtextformel"

    def description(self) -> str:
        return "Wiener Sachtextformel - German readability formula with 4 variants."

    def supported_languages(self) -> list[str]:
        return ["de-1996", "de-1901", "de-ch-1901"]

    def calculate(self, stats: TextStatistics, language: Language) -> FormulaResult:
        return self.calculate_variant(stats, language, 1)

    def calculate_variant(self, stats: TextStatistics, language: Language, variant: int) -> FormulaResult:
        data = self._compute(variant, stats)
        return FormulaResult(
            formula_name=f"{self.name()}_{variant}",
            language_code=language.code,
            score=data["score"],
            grade_level=data["gradeLevel"],
            interpretation=self._interpret(data["score"]),
            inputs=data["inputs"],
        )

    def _compute(self, variant: int, stats: TextStatistics) -> _ComputeResult:
        word_count = stats.word_count if stats.word_count > 0 else 1

        ms = (stats.polysyllable_count / word_count) * 100.0
        sl = stats.average_words_per_sentence
        iw = self._long_word_pct(stats, 6)
        es = 0.0

        if variant == 1:
            es = self._one_syllable_pct(stats)
            score = 0.1935 * ms + 0.1672 * sl + 0.1297 * iw - 0.0327 * es - 0.875
        elif variant == 2:
            score = 0.2007 * ms + 0.1682 * sl + 0.1373 * iw - 2.779
        elif variant == 3:
            score = 0.2963 * ms + 0.1905 * sl - 1.1144
        elif variant == 4:
            score = 0.2744 * ms + 0.2656 * sl - 1.693
        else:
            raise ValueError(
                f"Wiener Sachtextformel variant must be 1-4, got {variant}."
            )

        grade_level = min(max(score, 4.0), 15.0)

        return {
            "score": round(score, 1),
            "gradeLevel": grade_level,
            "inputs": {"ms": ms, "sl": sl, "iw": iw, "es": es, "variant": variant},
        }

    @staticmethod
    def _long_word_pct(stats: TextStatistics, threshold: int) -> float:
        return (stats.long_word_count / stats.word_count) * 100.0 if stats.word_count > 0 else 0.0

    @staticmethod
    def _one_syllable_pct(stats: TextStatistics) -> float:
        one_syllable = stats.syllable_histogram.get(1, 0)
        return (one_syllable / stats.word_count) * 100.0 if stats.word_count > 0 else 0.0

    @staticmethod
    def _interpret(score: float) -> str:
        if score < 5.0:
            return "Very Easy"
        elif score < 7.0:
            return "Easy"
        elif score < 9.0:
            return "Standard"
        elif score < 11.0:
            return "Fairly Hard"
        elif score < 13.0:
            return "Hard"
        else:
            return "Very Hard"
