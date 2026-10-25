class Armor:
    def __init__(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Броня должна быть целым числом")
        if value < 0:
            raise ValueError("Броня не может быть отрицательной")
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def reduce_damage(self, damage: int) -> int:
        if damage < 0:
            raise ValueError("Урон не может быть отрицательным")
        return max(damage - self._value, 0)

    def __repr__(self) -> str:
        return f"Armor({self._value})"
