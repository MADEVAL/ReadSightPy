from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..exceptions import UnsupportedLanguageException
from .language import Language
from .language_code import LanguageCode
from .language_repository import LanguageRepository


class JsonLanguageRepository(LanguageRepository):
    def __init__(self, languages_dir: str) -> None:
        self._languages_dir = languages_dir
        self._cache: dict[str, Language] = {}

    def find(self, language_code: str) -> Language:
        normalized = LanguageCode._normalize(language_code)

        if normalized in self._cache:
            return self._cache[normalized]

        file_path = Path(self._languages_dir) / f"{normalized}.json"
        if not file_path.is_file():
            raise UnsupportedLanguageException.with_code(language_code)

        data: dict[str, Any] = json.loads(file_path.read_text(encoding="utf-8"))
        language = Language.from_dict(data)
        self._cache[normalized] = language
        return language

    def list_codes(self) -> list[str]:
        path = Path(self._languages_dir)
        if not path.is_dir():
            raise RuntimeError(f'Failed to list language files in directory "{self._languages_dir}".')
        codes = sorted(p.stem for p in path.glob("*.json"))
        return codes

    def exists(self, language_code: str) -> bool:
        normalized = LanguageCode._normalize(language_code)
        if normalized in self._cache:
            return True
        return (Path(self._languages_dir) / f"{normalized}.json").is_file()
