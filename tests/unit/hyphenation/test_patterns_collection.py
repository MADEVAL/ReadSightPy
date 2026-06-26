from __future__ import annotations

from readsight.hyphenation.pattern import Pattern
from readsight.hyphenation.patterns_collection import PatternsCollection


class TestPatternsCollection:
    def test_add_and_get_weights(self) -> None:
        pc = PatternsCollection()
        pc.add(Pattern(["a", "b"], [0, 4, 0]))
        assert pc.get_weights("ab") == "040"

    def test_max_length(self) -> None:
        pc = PatternsCollection()
        pc.add(Pattern(["a"], [0, 0]))
        pc.add(Pattern(["a", "b", "c"], [0, 0, 4, 0]))
        assert pc.max_length() == 3

    def test_count(self) -> None:
        pc = PatternsCollection()
        pc.add(Pattern(["a"], [0, 0]))
        pc.add(Pattern(["b"], [0, 0]))
        assert pc.count() == 2

    def test_is_empty(self) -> None:
        pc = PatternsCollection()
        assert pc.is_empty() is True
        pc.add(Pattern(["a"], [0, 0]))
        assert pc.is_empty() is False

    def test_get_weights_missing(self) -> None:
        pc = PatternsCollection()
        assert pc.get_weights("nonexistent") is None

    def test_all_returns_copy(self) -> None:
        pc = PatternsCollection()
        pc.add(Pattern(["x", "y"], [1, 2, 3]))
        all_patterns = pc.all()
        assert all_patterns == {"xy": "123"}
