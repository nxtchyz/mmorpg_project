from game.factories.unit_factory import UnitFactory
from game.units.heavy_archer import HeavyArcher
from game.units.light_archer import LightArcher
from game.units.unit import Unit
from game.units.unit_kind import UnitKind


class ArcherFactory(UnitFactory):
    def create_unit(self, kind: UnitKind, x: int = 0, y: int = 0) -> Unit:
        match kind:
            case UnitKind.LIGHT_ARCHER:
                return LightArcher(x, y)
            case UnitKind.HEAVY_ARCHER:
                return HeavyArcher(x, y)
        raise ValueError(f"Фабрика лучников не создаёт юнитов вида {kind.value}")

    def supported_kinds(self) -> tuple[UnitKind, ...]:
        return UnitKind.LIGHT_ARCHER, UnitKind.HEAVY_ARCHER
