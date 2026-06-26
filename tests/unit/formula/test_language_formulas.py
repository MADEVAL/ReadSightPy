from __future__ import annotations

from readsight.formula.crawford import Crawford
from readsight.formula.fernandez_huerta import FernandezHuerta
from readsight.formula.flesch_kincaid_grade_level import FleschKincaidGradeLevel
from readsight.formula.flesch_reading_ease import FleschReadingEase
from readsight.formula.fog_pl import FogPL
from readsight.formula.gulpease import Gulpease
from readsight.formula.gutierrez_polini import GutierrezPolini
from readsight.formula.osman import Osman
from readsight.formula.szigriszt_pazos import SzigrisztPazos
from readsight.formula.wiener_sachtextformel import WienerSachtextformel
from readsight.language.language import Language
from readsight.text.text_statistics import TextStatistics


def _make_language(code: str, formula_configs: dict | None = None) -> Language:
    return Language.from_dict({
        "code": code,
        "name": code,
        "nativeName": code,
        "script": "Latin",
        "hyphenMins": {"left": 2, "right": 2},
        "letterPattern": "[A-Za-z]",
        "wordSplitPattern": "[^\\p{L}'’-]+",
        "sentenceBoundaryPattern": "[.!?]+",
        "formulas": formula_configs or {},
    })


def _make_stats(**overrides: float | int | dict[int, int]) -> TextStatistics:
    defaults: dict = {
        "letter_count": 200, "word_count": 50, "sentence_count": 5,
        "syllable_count": 75, "polysyllable_count": 5,
        "average_syllables_per_word": 1.5, "average_words_per_sentence": 10.0,
        "long_word_count": 8,
        "syllable_histogram": {1: 30, 2: 15, 3: 5},
    }
    defaults.update(overrides)
    return TextStatistics(**defaults)  # type: ignore[arg-type]


class TestFleschReadingEase:
    def test_english_default_coefficients(self) -> None:
        formula = FleschReadingEase()
        result = formula.calculate(_make_stats(), _make_language("en-us"))
        assert result.score > 0.0
        assert result.grade_level is None

    def test_german_coefficients(self) -> None:
        formula = FleschReadingEase()
        lang = _make_language("de-1996", {
            "flesch_reading_ease": {"enabled": True, "base": 180, "aslMult": 1.0, "aswMult": 58.5},
        })
        result = formula.calculate(_make_stats(), lang)
        english_result = formula.calculate(_make_stats(), _make_language("en-us"))
        assert result.score != english_result.score


class TestFleschKincaidGradeLevel:
    def test_calculation(self) -> None:
        formula = FleschKincaidGradeLevel()
        result = formula.calculate(_make_stats(), _make_language("en-us"))
        assert result.grade_level is not None
        assert "asl" in result.inputs


class TestGulpease:
    def test_calculation(self) -> None:
        formula = Gulpease()
        result = formula.calculate(_make_stats(), _make_language("it"))
        assert result.score != 0.0
        assert "letterCount" in result.inputs


class TestWienerSachtextformel:
    def test_variant_1(self) -> None:
        formula = WienerSachtextformel()
        result = formula.calculate_variant(_make_stats(), _make_language("de-1996"), 1)
        assert result.formula_name == "wiener_sachtextformel_1"
        assert result.grade_level is not None

    def test_variant_2(self) -> None:
        formula = WienerSachtextformel()
        result = formula.calculate_variant(_make_stats(), _make_language("de-1996"), 2)
        assert result.formula_name == "wiener_sachtextformel_2"

    def test_variant_3(self) -> None:
        formula = WienerSachtextformel()
        result = formula.calculate_variant(_make_stats(), _make_language("de-1996"), 3)
        assert result.formula_name == "wiener_sachtextformel_3"

    def test_variant_4(self) -> None:
        formula = WienerSachtextformel()
        result = formula.calculate_variant(_make_stats(), _make_language("de-1996"), 4)
        assert result.formula_name == "wiener_sachtextformel_4"

    def test_invalid_variant(self) -> None:
        import pytest

        formula = WienerSachtextformel()
        with pytest.raises(ValueError):
            formula.calculate_variant(_make_stats(), _make_language("de-1996"), 5)

    def test_default_is_variant_1(self) -> None:
        formula = WienerSachtextformel()
        result_default = formula.calculate(_make_stats(), _make_language("de-1996"))
        result_v1 = formula.calculate_variant(_make_stats(), _make_language("de-1996"), 1)
        assert result_default.score == result_v1.score


class TestFernandezHuerta:
    def test_calculation(self) -> None:
        formula = FernandezHuerta()
        result = formula.calculate(_make_stats(), _make_language("es"))
        assert result.score > 0.0


class TestSzigrisztPazos:
    def test_calculation(self) -> None:
        formula = SzigrisztPazos()
        result = formula.calculate(_make_stats(), _make_language("es"))
        assert result.score != 0.0
        assert "syllablesPer100" in result.inputs


class TestGutierrezPolini:
    def test_calculation(self) -> None:
        formula = GutierrezPolini()
        result = formula.calculate(_make_stats(), _make_language("es"))
        assert result.score != 0.0


class TestCrawford:
    def test_calculation(self) -> None:
        formula = Crawford()
        result = formula.calculate(_make_stats(), _make_language("es"))
        assert result.score != 0.0


class TestFogPL:
    def test_calculation(self) -> None:
        formula = FogPL()
        result = formula.calculate(_make_stats(), _make_language("pl"))
        assert result.score > 0.0
        assert result.grade_level is not None


class TestOsman:
    def test_calculation(self) -> None:
        formula = Osman()
        result = formula.calculate(_make_stats(), _make_language("ar"))
        assert result.score != 0.0
        assert "avgLetters" in result.inputs
