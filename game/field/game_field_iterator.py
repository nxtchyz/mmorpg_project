from typing import TYPE_CHECKING

from game.units.unit import Unit

if TYPE_CHECKING:
    from game.field.game_field import GameField


class GameFieldIterator:
    def __init__(self, field: "GameField") -> None:
        self._field = field
        self._index = 0

    def has_next(self) -> bool:
        total = self._field.width * self._field.height
        while self._index < total:
            if self._field.get_unit(*self._current_cell()) is not None:
                return True
            self._index += 1
        return False

    def next(self) -> Unit:
        if not self.has_next():
            raise StopIteration
        unit = self._field.get_unit(*self._current_cell())
        self._index += 1
        return unit

    def _current_cell(self) -> tuple[int, int]:
        return self._index % self._field.width, self._index // self._field.width

    def __iter__(self) -> "GameFieldIterator":
        return self

    def __next__(self) -> Unit:
        return self.next()
