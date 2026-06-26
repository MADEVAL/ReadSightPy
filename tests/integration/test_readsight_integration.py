from __future__ import annotations

from readsight import ReadSight
from tests.conftest import FIXTURES_DIR


class TestReadSightIntegration:
    def test_engine_creation_en_us(self) -> None:
        rs = ReadSight("en-us")
        assert rs.language.code == "en-us"
        assert rs.language.name == "English (US)"

    def test_engine_creation_de(self) -> None:
        rs = ReadSight("de-1996")
        assert rs.language.code == "de-1996"

    def test_engine_creation_ru(self) -> None:
        rs = ReadSight("ru")
        assert rs.language.code == "ru"

    def test_get_supported_languages(self) -> None:
        langs = ReadSight.get_supported_languages()
        assert "en-us" in langs
        assert "ru" in langs
        assert "de-1996" in langs
        assert len(langs) >= 86

    def test_get_supported_formulas(self) -> None:
        rs = ReadSight("en-us")
        formulas = rs.get_supported_formulas()
        assert "gunning_fog" in formulas
        assert "flesch_reading_ease" in formulas
        assert "ari" in formulas

    def test_syllable_count_banana(self) -> None:
        rs = ReadSight("en-us")
        assert rs.syllable_count("banana") == 3

    def test_syllable_count_hyphenation(self) -> None:
        rs = ReadSight("en-us")
        assert rs.syllable_count("hyphenation") == 4

    def test_syllable_count_hello(self) -> None:
        rs = ReadSight("en-us")
        assert rs.syllable_count("hello") == 2

    def test_split_word(self) -> None:
        rs = ReadSight("en-us")
        parts = rs.split_word("hyphenation")
        assert len(parts) >= 3

    def test_analyze_moby_dick(self) -> None:
        rs = ReadSight("en-us")
        text = (FIXTURES_DIR / "text" / "moby-dick-opening.txt").read_text(encoding="utf-8")
        stats = rs.analyze(text)
        assert stats.word_count > 50
        assert stats.sentence_count > 1
        assert stats.letter_count > 200
        assert stats.syllable_count > 100

    def test_gunning_fog(self) -> None:
        rs = ReadSight("en-us")
        text = "The quick brown fox jumps over the lazy dog. This is a simple sentence for testing."
        result = rs.gunning_fog(text)
        assert result.score > 0.0
        assert result.formula_name == "gunning_fog"
        assert result.language_code == "en-us"
        assert isinstance(result.interpretation, str)
        assert "asl" in result.inputs

    def test_flesch_reading_ease(self) -> None:
        rs = ReadSight("en-us")
        text = "The cat sat on the mat. It was a very good day."
        result = rs.flesch_reading_ease(text)
        assert result.score > 0.0
        assert result.formula_name == "flesch_reading_ease"

    def test_flesch_kincaid_grade_level(self) -> None:
        rs = ReadSight("en-us")
        text = "The quick brown fox jumps over the lazy dog."
        result = rs.flesch_kincaid_grade_level(text)
        assert isinstance(result.score, float)
        assert result.grade_level is not None

    def test_smog_index(self) -> None:
        rs = ReadSight("en-us")
        text = "This is a test. It has a few sentences. Here is a polysyllabic word like complicated or sophisticated."
        result = rs.smog_index(text)
        assert result.score > 0.0

    def test_coleman_liau(self) -> None:
        rs = ReadSight("en-us")
        text = "The cat sat on the mat."
        result = rs.coleman_liau(text)
        assert isinstance(result.score, float)
        assert result.grade_level is not None

    def test_ari(self) -> None:
        rs = ReadSight("en-us")
        text = "Testing the automated readability index. It uses character counts."
        result = rs.automated_readability_index(text)
        assert result.score != 0.0

    def test_lix(self) -> None:
        rs = ReadSight("en-us")
        text = "This is a simple text for LIX testing. It has a few sentences."
        result = rs.lix(text)
        assert result.score > 0.0

    def test_dale_chall(self) -> None:
        rs = ReadSight("en-us")
        text = "The boy ran to the store. He wanted some candy and a toy."
        result = rs.dale_chall(text)
        assert result.score > 0.0

    def test_spache(self) -> None:
        rs = ReadSight("en-us")
        text = "The cat sat on the mat. The dog ran to the park."
        result = rs.spache(text)
        assert result.score > 0.0

    def test_wiener_sachtextformel(self) -> None:
        rs = ReadSight("de-1996")
        text = "Dies ist ein einfacher deutscher Text. Er hat mehrere Sätze für den Test."
        result = rs.wiener_sachtextformel(text, variant=1)
        assert result.score > 0.0

    def test_gulpease(self) -> None:
        rs = ReadSight("it")
        text = "Questo è un semplice testo italiano. Serve per testare la formula Gulpease."
        result = rs.gulpease(text)
        assert result.score > 0.0

    def test_fernandez_huerta(self) -> None:
        rs = ReadSight("es")
        text = "Este es un texto simple en español. Sirve para probar la fórmula."
        result = rs.fernandez_huerta(text)
        assert result.score > 0.0

    def test_szigriszt_pazos(self) -> None:
        rs = ReadSight("es")
        text = "Texto de prueba para la fórmula Szigriszt-Pazos en español."
        result = rs.szigriszt_pazos(text)
        assert result.score > 0.0

    def test_gutierrez_polini(self) -> None:
        rs = ReadSight("es")
        text = "Prueba de comprensibilidad para Gutierrez Polini."
        result = rs.gutierrez_polini(text)
        assert result.score > 0.0

    def test_crawford(self) -> None:
        rs = ReadSight("es")
        text = "Texto escolar para probar la fórmula Crawford."
        result = rs.crawford(text)
        assert result.score != 0.0

    def test_fog_pl(self) -> None:
        rs = ReadSight("pl")
        text = "To jest prosty polski tekst do testowania formuły FOG-PL."
        result = rs.fog_pl(text)
        assert result.score > 0.0

    def test_osman(self) -> None:
        rs = ReadSight("ar")
        text = "هذا نص عربي بسيط لاختبار معادلة عثمان للقراءة."
        result = rs.osman(text)
        assert result.score != 0.0

    def test_generic_score(self) -> None:
        rs = ReadSight("en-us")
        text = "The quick brown fox. Simple sentences for testing."
        result = rs.score("gunning_fog", text)
        assert result.score > 0.0
        assert result.formula_name == "gunning_fog"

    def test_unsupported_formula_raises(self) -> None:
        import pytest

        from readsight.exceptions import UnsupportedFormulaException

        rs = ReadSight("en-us")
        with pytest.raises(UnsupportedFormulaException):
            rs.score("gulpease", "some text")

    def test_add_hyphenations(self) -> None:
        rs = ReadSight("en-us")
        rs.add_hyphenations({"testword": "test-word"})
        parts = rs.split_word("testword")
        assert parts == ["test", "word"]

    def test_histogram_syllables(self) -> None:
        rs = ReadSight("en-us")
        hist = rs.histogram_syllables("cat dog banana extraordinary")
        assert isinstance(hist, dict)
        assert len(hist) > 0

    def test_flesch_russian(self) -> None:
        rs = ReadSight("ru")
        text = "Это простой русский текст для тестирования формулы читаемости."
        result = rs.flesch_reading_ease(text)
        assert result.score > 0.0
        assert result.language_code == "ru"
