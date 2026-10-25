from game.attributes.armor import Armor


class Attack:
    def __init__(self, value: int) -> None:
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def calculate_damage(self, target_armor: Armor) -> int:
        raise NotImplementedError
