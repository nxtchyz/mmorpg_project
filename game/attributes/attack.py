from game.attributes.armor import Armor


class Attack:
    def __init__(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Атака должна быть целым числом")
        if value < 0:
            raise ValueError("Атака не может быть отрицательной")
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def calculate_damage(self, target_armor: Armor) -> int:
        return target_armor.reduce_damage(self._value)

    def __repr__(self) -> str:
        return f"Attack({self._value})"
