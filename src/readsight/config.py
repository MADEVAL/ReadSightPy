from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Config:
    patterns_dir: str
    languages_dir: str
    cache_dir: str

    @classmethod
    def default(cls) -> Config:
        import platformdirs

        pkg_dir = Path(__file__).resolve().parent
        return cls(
            patterns_dir=str(pkg_dir / "data" / "patterns"),
            languages_dir=str(pkg_dir / "data" / "languages"),
            cache_dir=str(Path(platformdirs.user_cache_dir("readsight", ensure_exists=True))),
        )
