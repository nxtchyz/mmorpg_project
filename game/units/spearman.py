from copy import deepcopy

from game.attributes.armor import Armor
from game.attributes.attack import Attack
from game.attributes.health import Health
from game.units.infantry import Infantry


class Spearman(Infantry):
    def __init__(self, x: int = 0, y: int = 0) -> None:
        super().__init__(Health(110), Armor(5), Attack(17), attack_range=2, x=x, y=y)

    def get_type(self) -> str:
        return "Копейщик"

    def get_symbol(self) -> str:
        return "P"

    def clone(self) -> "Spearman":
        return deepcopy(self)
