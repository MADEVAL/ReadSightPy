from __future__ import annotations

from pathlib import Path

from readsight.language.json_language_repository import JsonLanguageRepository
from readsight.language.language import Language


class TestJsonLanguageRepository:
    def test_find_and_cache(self) -> None:
        repo = JsonLanguageRepository(str(Path("src/readsight/data/languages")))
        lang = repo.find("en-us")
        assert isinstance(lang, Language)
        assert lang.code == "en-us"
        cached = repo.find("en-us")
        assert cached is lang

    def test_list_codes(self) -> None:
        repo = JsonLanguageRepository(str(Path("src/readsight/data/languages")))
        codes = repo.list_codes()
        assert "en-us" in codes
        assert "ru" in codes
        assert len(codes) >= 86

    def test_exists(self) -> None:
        repo = JsonLanguageRepository(str(Path("src/readsight/data/languages")))
        assert repo.exists("en-us") is True
        assert repo.exists("nonexistent-zz") is False

    def test_find_unsupported_language(self) -> None:
        import pytest

        from readsight.exceptions import UnsupportedLanguageException

        repo = JsonLanguageRepository(str(Path("src/readsight/data/languages")))
        with pytest.raises(UnsupportedLanguageException):
            repo.find("zz-nonexistent")
