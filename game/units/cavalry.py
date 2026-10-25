from game.attributes.armor import Armor
from game.attributes.attack import Attack
from game.attributes.health import Health
from game.units.unit import Unit


class Cavalry(Unit):
    SPEED = 4

    def __init__(
        self,
        health: Health,
        armor: Armor,
        attack: Attack,
        attack_range: int = 1,
        x: int = 0,
        y: int = 0,
    ) -> None:
        super().__init__(health, armor, attack, self.SPEED, attack_range, x, y)

    def get_category(self) -> str:
        return "Конница"
