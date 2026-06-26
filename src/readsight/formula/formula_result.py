from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class FormulaResult:
    formula_name: str
    language_code: str
    score: float
    grade_level: float | None
    interpretation: str
    inputs: dict[str, float | int] = field(default_factory=dict)
