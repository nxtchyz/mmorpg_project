from abc import ABC, abstractmethod

from game.units.unit import Unit
from game.units.unit_kind import UnitKind


class UnitFactory(ABC):
    @abstractmethod
    def create_unit(self, kind: UnitKind, x: int = 0, y: int = 0) -> Unit:
        ...

    @abstractmethod
    def supported_kinds(self) -> tuple[UnitKind, ...]:
        ...

    def supports(self, kind: UnitKind) -> bool:
        return kind in self.supported_kinds()
