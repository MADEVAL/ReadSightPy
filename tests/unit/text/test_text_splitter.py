from __future__ import annotations

from readsight.language.language import Language
from readsight.text.text_splitter import TextSplitter


def _make_language(**overrides: object) -> Language:
    data: dict = {
        "code": "en-us",
        "name": "English",
        "nativeName": "English",
        "script": "Latin",
        "hyphenMins": {"left": 2, "right": 2},
        "letterPattern": "[A-Za-z]",
        "wordSplitPattern": "[^\\p{L}'’-]+",
        "sentenceBoundaryPattern": "[.!?]+",
    }
    data.update(overrides)  # type: ignore[arg-type]
    return Language.from_dict(data)  # type: ignore[arg-type]


class TestTextSplitter:
    def test_split_words(self) -> None:
        lang = _make_language()
        ts = TextSplitter(lang)
        result = ts.split_words("The quick brown fox")
        assert result == ["The", "quick", "brown", "fox"]

    def test_split_words_handles_apostrophe(self) -> None:
        lang = _make_language()
        ts = TextSplitter(lang)
        result = ts.split_words("don't can't it's")
        assert "don't" in result

    def test_split_words_empty(self) -> None:
        lang = _make_language()
        ts = TextSplitter(lang)
        assert ts.split_words("") == []
        assert ts.split_words("   ") == []

    def test_split_sentences(self) -> None:
        lang = _make_language()
        ts = TextSplitter(lang)
        result = ts.split_sentences("Hello world. How are you?")
        assert len(result) == 2

    def test_count_letters(self) -> None:
        lang = _make_language()
        ts = TextSplitter(lang)
        assert ts.count_letters("Hello world") == 10

    def test_count_letters_empty(self) -> None:
        lang = _make_language()
        ts = TextSplitter(lang)
        assert ts.count_letters("") == 0

    def test_count_words(self) -> None:
        lang = _make_language()
        ts = TextSplitter(lang)
        assert ts.count_words("one two three") == 3

    def test_count_sentences(self) -> None:
        lang = _make_language()
        ts = TextSplitter(lang)
        assert ts.count_sentences("Hi there. How goes?") == 2

    def test_count_sentences_no_boundary(self) -> None:
        lang = _make_language()
        ts = TextSplitter(lang)
        assert ts.count_sentences("just words") == 1

    def test_count_long_words(self) -> None:
        lang = _make_language()
        ts = TextSplitter(lang)
        assert ts.count_long_words("a bb ccc dddd eeeee", 3) == 2

    def test_russian_letters(self) -> None:
        lang = _make_language(
            code="ru",
            letterPattern="[А-Яа-яЁё]",
        )
        ts = TextSplitter(lang)
        assert ts.count_letters("Привет мир") == 9
