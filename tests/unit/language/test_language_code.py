from __future__ import annotations

from readsight.language.language_code import LanguageCode


class TestLanguageCode:
    def test_normalize_lowercase(self) -> None:
        lc = LanguageCode("EN-US")
        assert lc.value == "en-us"

    def test_normalize_trim(self) -> None:
        lc = LanguageCode("  de-1996  ")
        assert lc.value == "de-1996"

    def test_equality(self) -> None:
        a = LanguageCode("en-us")
        b = LanguageCode("EN-US")
        assert a == b

    def test_inequality(self) -> None:
        a = LanguageCode("en-us")
        b = LanguageCode("de-1996")
        assert a != b

    def test_hash_consistent(self) -> None:
        a = LanguageCode("EN-us")
        b = LanguageCode("en-US")
        assert hash(a) == hash(b)

    def test_str(self) -> None:
        lc = LanguageCode("en-us")
        assert str(lc) == "en-us"
