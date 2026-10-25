from copy import deepcopy

from game.attributes.armor import Armor
from game.attributes.attack import Attack
from game.attributes.health import Health
from game.units.cavalry import Cavalry


class Cataphract(Cavalry):
    def __init__(self, x: int = 0, y: int = 0) -> None:
        super().__init__(Health(160), Armor(12), Attack(25), attack_range=1, x=x, y=y)

    def get_type(self) -> str:
        return "Катафракт"

    def get_symbol(self) -> str:
        return "C"

    def clone(self) -> "Cataphract":
        return deepcopy(self)
