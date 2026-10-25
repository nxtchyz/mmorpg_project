from game.units.unit import Unit


class GameField:
    def __init__(self, width: int, height: int, max_units: int) -> None:
        self._width = width
        self._height = height
        self._max_units = max_units
        self._cells: list[list[Unit | None]] = [[None] * width for _ in range(height)]
        self._count = 0

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def max_units(self) -> int:
        return self._max_units

    def is_inside(self, x: int, y: int) -> bool:
        raise NotImplementedError

    def is_free(self, x: int, y: int) -> bool:
        raise NotImplementedError

    def is_full(self) -> bool:
        raise NotImplementedError

    def add_unit(self, unit: Unit) -> None:
        raise NotImplementedError

    def remove_unit(self, x: int, y: int) -> Unit:
        raise NotImplementedError

    def get_unit(self, x: int, y: int) -> Unit | None:
        raise NotImplementedError

    def move_unit(self, from_x: int, from_y: int, to_x: int, to_y: int) -> None:
        raise NotImplementedError

    def size(self) -> int:
        raise NotImplementedError

    def empty(self) -> bool:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        return self.size()
