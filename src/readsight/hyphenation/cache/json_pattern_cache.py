from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..hyphenation_exceptions_collection import HyphenationExceptionsCollection
from ..hyphenation_override import HyphenationOverride
from ..pattern import Pattern
from ..patterns_collection import PatternsCollection
from .pattern_cache import PatternCache

_CACHE_VERSION = "2.0"


class JsonPatternCache(PatternCache):
    def __init__(self, cache_dir: str) -> None:
        self._cache_dir = cache_dir

    def has(self, language_code: str) -> bool:
        return Path(self._get_file_path(language_code)).is_file()

    def get(self, language_code: str) -> dict[str, Any] | None:
        file_path = self._get_file_path(language_code)
        path = Path(file_path)
        if not path.is_file():
            return None

        try:
            data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None

        if data.get("version") != _CACHE_VERSION:
            return None

        patterns = PatternsCollection()
        for p in data["patterns"]:
            patterns.add(Pattern(p["chars"], p["weights"]))

        exceptions = HyphenationExceptionsCollection()
        for word, hyphenated in data.get("exceptions", {}).items():
            exceptions.add(HyphenationOverride(str(word), str(hyphenated)))

        return {
            "patterns": patterns,
            "exceptions": exceptions,
            "maxPatternLength": data["maxPatternLength"],
        }

    def set(self, language_code: str, data: dict[str, Any]) -> None:
        patterns_col: PatternsCollection = data["patterns"]
        exceptions_col: HyphenationExceptionsCollection = data["exceptions"]

        payload: dict[str, Any] = {
            "version": _CACHE_VERSION,
            "patterns": self._serialize_patterns(patterns_col),
            "exceptions": exceptions_col.all(),
            "maxPatternLength": data["maxPatternLength"],
        }

        cache_path = Path(self._get_file_path(language_code))
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    def clear(self, language_code: str) -> None:
        path = Path(self._get_file_path(language_code))
        if path.is_file():
            path.unlink()

    def clear_all(self) -> None:
        cache_dir = Path(self._cache_dir)
        if cache_dir.is_dir():
            for f in cache_dir.glob("*.json"):
                f.unlink()

    def _get_file_path(self, language_code: str) -> str:
        return str(Path(self._cache_dir) / f"syllable.{language_code}.json")

    @staticmethod
    def _serialize_patterns(collection: PatternsCollection) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for key, weights in collection.all().items():
            chars = list(key)
            weight_values = [int(d) for d in weights]
            result.append({"chars": chars, "weights": weight_values})
        return result
