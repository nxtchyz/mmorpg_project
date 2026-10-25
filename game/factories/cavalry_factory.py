from game.factories.unit_factory import UnitFactory
from game.units.cataphract import Cataphract
from game.units.horse_archer import HorseArcher
from game.units.unit import Unit
from game.units.unit_kind import UnitKind


class CavalryFactory(UnitFactory):
    def create_unit(self, kind: UnitKind, x: int = 0, y: int = 0) -> Unit:
        match kind:
            case UnitKind.CATAPHRACT:
                return Cataphract(x, y)
            case UnitKind.HORSE_ARCHER:
                return HorseArcher(x, y)
        raise ValueError(f"Фабрика конницы не создаёт юнитов вида {kind.value}")

    def supported_kinds(self) -> tuple[UnitKind, ...]:
        return UnitKind.CATAPHRACT, UnitKind.HORSE_ARCHER
