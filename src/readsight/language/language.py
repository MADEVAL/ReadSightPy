from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..language.script import Script


@dataclass(frozen=True, slots=True)
class Language:
    code: str
    name: str
    native_name: str
    script: Script
    min_hyphen_left: int
    min_hyphen_right: int
    letter_pattern: str
    word_split_pattern: str
    sentence_boundary_pattern: str
    formula_configs: dict[str, dict[str, Any]] = field(default_factory=dict)
    syllable_heuristics: dict[str, Any] | None = None
    syllable_mode: str = "tex"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Language:
        return cls(
            code=data["code"],
            name=data["name"],
            native_name=data["nativeName"],
            script=Script(data["script"]),
            min_hyphen_left=data["hyphenMins"]["left"],
            min_hyphen_right=data["hyphenMins"]["right"],
            letter_pattern=data["letterPattern"],
            word_split_pattern=data["wordSplitPattern"],
            sentence_boundary_pattern=data["sentenceBoundaryPattern"],
            formula_configs=data.get("formulas", {}),
            syllable_heuristics=data.get("syllableHeuristics"),
            syllable_mode=data.get("syllableMode", "tex"),
        )

    def supports_formula(self, formula_name: str) -> bool:
        return formula_name in self.formula_configs

    def get_formula_config(self, formula_name: str) -> dict[str, Any] | None:
        return self.formula_configs.get(formula_name)

    def get_supported_formulas(self) -> list[str]:
        return list(self.formula_configs.keys())
