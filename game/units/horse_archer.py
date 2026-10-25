from copy import deepcopy

from game.attributes.armor import Armor
from game.attributes.attack import Attack
from game.attributes.health import Health
from game.units.cavalry import Cavalry


class HorseArcher(Cavalry):
    def __init__(self, x: int = 0, y: int = 0) -> None:
        super().__init__(Health(100), Armor(4), Attack(16), attack_range=4, x=x, y=y)

    def get_type(self) -> str:
        return "Конный лучник"

    def get_symbol(self) -> str:
        return "A"

    def clone(self) -> "HorseArcher":
        return deepcopy(self)
