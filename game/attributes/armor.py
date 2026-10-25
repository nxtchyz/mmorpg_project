class Armor:
    def __init__(self, value: int) -> None:
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def reduce_damage(self, damage: int) -> int:
        raise NotImplementedError
