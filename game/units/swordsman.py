from copy import deepcopy

from game.attributes.armor import Armor
from game.attributes.attack import Attack
from game.attributes.health import Health
from game.units.infantry import Infantry


class Swordsman(Infantry):
    def __init__(self, x: int = 0, y: int = 0) -> None:
        super().__init__(Health(120), Armor(6), Attack(20), attack_range=1, x=x, y=y)

    def get_type(self) -> str:
        return "Мечник"

    def get_symbol(self) -> str:
        return "S"

    def clone(self) -> "Swordsman":
        return deepcopy(self)
