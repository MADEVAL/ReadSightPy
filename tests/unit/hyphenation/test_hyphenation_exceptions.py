from __future__ import annotations

from readsight.hyphenation.hyphenation_exceptions_collection import HyphenationExceptionsCollection
from readsight.hyphenation.hyphenation_override import HyphenationOverride


class TestHyphenationExceptionsCollection:
    def test_add_and_has(self) -> None:
        ec = HyphenationExceptionsCollection()
        ec.add(HyphenationOverride("test", "te-st"))
        assert ec.has("test") is True
        assert ec.has("nonexistent") is False

    def test_get(self) -> None:
        ec = HyphenationExceptionsCollection()
        ec.add(HyphenationOverride("hello", "hel-lo"))
        assert ec.get("hello") == "hel-lo"
        assert ec.get("nope") is None

    def test_count(self) -> None:
        ec = HyphenationExceptionsCollection()
        assert ec.count() == 0
        ec.add(HyphenationOverride("a", "a"))
        ec.add(HyphenationOverride("b", "b"))
        assert ec.count() == 2

    def test_is_empty(self) -> None:
        ec = HyphenationExceptionsCollection()
        assert ec.is_empty() is True
        ec.add(HyphenationOverride("a", "a"))
        assert ec.is_empty() is False

    def test_all(self) -> None:
        ec = HyphenationExceptionsCollection()
        ec.add(HyphenationOverride("foo", "fo-o"))
        assert ec.all() == {"foo": "fo-o"}
