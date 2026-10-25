from copy import deepcopy

from game.attributes.armor import Armor
from game.attributes.attack import Attack
from game.attributes.health import Health
from game.units.archer import Archer


class HeavyArcher(Archer):
    def __init__(self, x: int = 0, y: int = 0) -> None:
        super().__init__(Health(90), Armor(5), Attack(22), attack_range=4, x=x, y=y)

    def get_type(self) -> str:
        return "Тяжёлый лучник"

    def get_symbol(self) -> str:
        return "H"

    def clone(self) -> "HeavyArcher":
        return deepcopy(self)
