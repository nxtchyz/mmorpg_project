class Health:
    def __init__(self, value: int) -> None:
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def decrease(self, amount: int) -> None:
        raise NotImplementedError

    def increase(self, amount: int) -> None:
        raise NotImplementedError

    def is_zero(self) -> bool:
        raise NotImplementedError
