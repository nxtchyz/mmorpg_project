from copy import deepcopy

from game.attributes.armor import Armor
from game.attributes.attack import Attack
from game.attributes.health import Health
from game.units.archer import Archer


class LightArcher(Archer):
    def __init__(self, x: int = 0, y: int = 0) -> None:
        super().__init__(Health(70), Armor(2), Attack(14), attack_range=5, x=x, y=y)

    def get_type(self) -> str:
        return "Лёгкий лучник"

    def get_symbol(self) -> str:
        return "L"

    def clone(self) -> "LightArcher":
        return deepcopy(self)
