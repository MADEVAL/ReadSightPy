from __future__ import annotations

from .automated_readability_index import AutomatedReadabilityIndex
from .coleman_liau import ColemanLiau
from .crawford import Crawford
from .dale_chall import DaleChall
from .fernandez_huerta import FernandezHuerta
from .flesch_kincaid_grade_level import FleschKincaidGradeLevel
from .flesch_reading_ease import FleschReadingEase
from .fog_pl import FogPL
from .formula_registry import FormulaRegistry
from .gulpease import Gulpease
from .gunning_fog import GunningFog
from .gutierrez_polini import GutierrezPolini
from .lix import Lix
from .osman import Osman
from .smog_index import SmogIndex
from .spache import Spache
from .szigriszt_pazos import SzigrisztPazos
from .wiener_sachtextformel import WienerSachtextformel


class FormulaRegistryFactory:
    @staticmethod
    def create() -> FormulaRegistry:
        registry = FormulaRegistry()
        registry.register(AutomatedReadabilityIndex())
        registry.register(ColemanLiau())
        registry.register(Crawford())
        registry.register(DaleChall())
        registry.register(FernandezHuerta())
        registry.register(FleschKincaidGradeLevel())
        registry.register(FleschReadingEase())
        registry.register(FogPL())
        registry.register(Gulpease())
        registry.register(GunningFog())
        registry.register(GutierrezPolini())
        registry.register(Lix())
        registry.register(Osman())
        registry.register(SmogIndex())
        registry.register(Spache())
        registry.register(SzigrisztPazos())
        registry.register(WienerSachtextformel())
        return registry
