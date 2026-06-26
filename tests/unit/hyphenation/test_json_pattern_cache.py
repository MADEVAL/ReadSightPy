from __future__ import annotations

import tempfile

from readsight.hyphenation.cache.json_pattern_cache import JsonPatternCache
from readsight.hyphenation.hyphenation_exceptions_collection import HyphenationExceptionsCollection
from readsight.hyphenation.hyphenation_override import HyphenationOverride
from readsight.hyphenation.pattern import Pattern
from readsight.hyphenation.patterns_collection import PatternsCollection


class TestJsonPatternCache:
    def test_set_and_get(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = JsonPatternCache(tmpdir)

            patterns = PatternsCollection()
            patterns.add(Pattern(["a", "b"], [0, 4, 0]))
            exceptions = HyphenationExceptionsCollection()
            exceptions.add(HyphenationOverride("test-word", "test-word"))

            cache.set("en-us", {
                "patterns": patterns,
                "exceptions": exceptions,
                "maxPatternLength": 2,
            })

            assert cache.has("en-us") is True

            result = cache.get("en-us")
            assert result is not None
            assert result["maxPatternLength"] == 2

            loaded_patterns: PatternsCollection = result["patterns"]
            assert loaded_patterns.count() == 1

    def test_has_returns_false(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = JsonPatternCache(tmpdir)
            assert cache.has("nonexistent") is False

    def test_get_returns_none_when_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = JsonPatternCache(tmpdir)
            assert cache.get("nonexistent") is None

    def test_clear(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = JsonPatternCache(tmpdir)
            patterns = PatternsCollection()
            cache.set("en-us", {
                "patterns": patterns,
                "exceptions": HyphenationExceptionsCollection(),
                "maxPatternLength": 0,
            })
            assert cache.has("en-us") is True
            cache.clear("en-us")
            assert cache.has("en-us") is False

    def test_clear_all(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = JsonPatternCache(tmpdir)
            patterns = PatternsCollection()
            empty_exc = HyphenationExceptionsCollection()
            cache.set("en-us", {"patterns": patterns, "exceptions": empty_exc, "maxPatternLength": 0})
            cache.set("ru", {"patterns": patterns, "exceptions": empty_exc, "maxPatternLength": 0})
            cache.clear_all()
            assert cache.has("en-us") is False
            assert cache.has("ru") is False
