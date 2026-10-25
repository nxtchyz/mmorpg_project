class Health:
    def __init__(self, value: int, max_value: int | None = None) -> None:
        if max_value is None:
            max_value = value
        if not isinstance(value, int) or not isinstance(max_value, int):
            raise TypeError("Здоровье должно быть целым числом")
        if max_value <= 0:
            raise ValueError("Максимальное здоровье должно быть положительным")
        if not 0 <= value <= max_value:
            raise ValueError("Здоровье должно быть в диапазоне от 0 до максимального")
        self._value = value
        self._max_value = max_value

    @property
    def value(self) -> int:
        return self._value

    @property
    def max_value(self) -> int:
        return self._max_value

    def decrease(self, amount: int) -> int:
        self._check_amount(amount)
        lost = min(amount, self._value)
        self._value -= lost
        return lost

    def increase(self, amount: int) -> int:
        self._check_amount(amount)
        restored = min(amount, self._max_value - self._value)
        self._value += restored
        return restored

    def is_zero(self) -> bool:
        return self._value == 0

    @staticmethod
    def _check_amount(amount: int) -> None:
        if not isinstance(amount, int):
            raise TypeError("Величина изменения здоровья должна быть целым числом")
        if amount < 0:
            raise ValueError("Величина изменения здоровья не может быть отрицательной")

    def __repr__(self) -> str:
        return f"Health({self._value}/{self._max_value})"
