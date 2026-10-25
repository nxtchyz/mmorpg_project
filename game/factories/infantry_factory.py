from game.factories.unit_factory import UnitFactory
from game.units.spearman import Spearman
from game.units.swordsman import Swordsman
from game.units.unit import Unit
from game.units.unit_kind import UnitKind


class InfantryFactory(UnitFactory):
    def create_unit(self, kind: UnitKind, x: int = 0, y: int = 0) -> Unit:
        match kind:
            case UnitKind.SWORDSMAN:
                return Swordsman(x, y)
            case UnitKind.SPEARMAN:
                return Spearman(x, y)
        raise ValueError(f"Фабрика пехоты не создаёт юнитов вида {kind.value}")

    def supported_kinds(self) -> tuple[UnitKind, ...]:
        return UnitKind.SWORDSMAN, UnitKind.SPEARMAN
