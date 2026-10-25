from collections.abc import Iterable
from copy import deepcopy

from game.factories.unit_factory import UnitFactory
from game.field.game_field_iterator import GameFieldIterator
from game.units.unit import Unit
from game.units.unit_kind import UnitKind


class GameField:
    def __init__(self, width: int, height: int, max_units: int) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("Размеры поля должны быть положительными")
        if not 0 < max_units <= width * height:
            raise ValueError("Лимит юнитов должен быть от 1 до количества клеток поля")
        self._width = width
        self._height = height
        self._max_units = max_units
        self._cells = self._empty_cells(width, height)
        self._count = 0

    @classmethod
    def from_moved(cls, other: "GameField") -> "GameField":
        field = cls(other.width, other.height, other.max_units)
        field.move_from(other)
        return field

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
        return 0 <= x < self._width and 0 <= y < self._height

    def is_free(self, x: int, y: int) -> bool:
        return self.is_inside(x, y) and self._cells[y][x] is None

    def is_full(self) -> bool:
        return self._count >= self._max_units

    def add_unit(self, unit: Unit) -> None:
        x, y = unit.position
        self._check_inside(x, y)
        if not self.is_free(x, y):
            raise ValueError(f"Клетка ({x}, {y}) уже занята")
        if self.is_full():
            raise OverflowError(f"На поле уже максимум юнитов: {self._max_units}")
        self._cells[y][x] = unit
        self._count += 1

    def populate(
        self,
        factory: UnitFactory,
        kind: UnitKind,
        positions: Iterable[tuple[int, int]],
    ) -> list[Unit]:
        if not factory.supports(kind):
            raise ValueError(f"Фабрика {type(factory).__name__} не создаёт юнитов вида {kind.value}")
        positions = list(positions)
        if len(set(positions)) != len(positions):
            raise ValueError("Позиции для размещения повторяются")
        if self._count + len(positions) > self._max_units:
            raise OverflowError(f"Не хватит места: свободно {self._max_units - self._count}, нужно {len(positions)}")
        for x, y in positions:
            if not self.is_free(x, y):
                raise ValueError(f"Клетка ({x}, {y}) занята или за пределами поля")
        units = [factory.create_unit(kind, x, y) for x, y in positions]
        for unit in units:
            self.add_unit(unit)
        return units

    def remove_unit(self, x: int, y: int) -> Unit:
        unit = self.get_unit(x, y)
        if unit is None:
            raise KeyError(f"На клетке ({x}, {y}) нет юнита")
        self._cells[y][x] = None
        self._count -= 1
        return unit

    def get_unit(self, x: int, y: int) -> Unit | None:
        self._check_inside(x, y)
        return self._cells[y][x]

    def move_unit(self, from_x: int, from_y: int, to_x: int, to_y: int) -> None:
        unit = self.get_unit(from_x, from_y)
        if unit is None:
            raise KeyError(f"На клетке ({from_x}, {from_y}) нет юнита")
        self._check_inside(to_x, to_y)
        if not self.is_free(to_x, to_y):
            raise ValueError(f"Клетка ({to_x}, {to_y}) уже занята")
        unit.move_to(to_x, to_y)
        self._cells[from_y][from_x] = None
        self._cells[to_y][to_x] = unit

    def size(self) -> int:
        return self._count

    def empty(self) -> bool:
        return self._count == 0

    def clear(self) -> None:
        self._cells = self._empty_cells(self._width, self._height)
        self._count = 0

    def copy(self) -> "GameField":
        field = GameField(self._width, self._height, self._max_units)
        for unit in self:
            field.add_unit(unit.clone())
        return field

    def assign(self, other: "GameField") -> None:
        if other is self:
            return
        self.move_from(other.copy())

    def move_from(self, other: "GameField") -> None:
        if other is self:
            return
        self._width = other._width
        self._height = other._height
        self._max_units = other._max_units
        self._cells = other._cells
        self._count = other._count
        other._cells = self._empty_cells(other._width, other._height)
        other._count = 0

    def _check_inside(self, x: int, y: int) -> None:
        if not self.is_inside(x, y):
            raise IndexError(f"Клетка ({x}, {y}) за пределами поля {self._width}x{self._height}")

    @staticmethod
    def _empty_cells(width: int, height: int) -> list[list[Unit | None]]:
        return [[None] * width for _ in range(height)]

    def __copy__(self) -> "GameField":
        return self.copy()

    def __deepcopy__(self, memo: dict) -> "GameField":
        field = self.copy()
        memo[id(self)] = field
        return field

    def __iter__(self) -> GameFieldIterator:
        return GameFieldIterator(self)

    def __len__(self) -> int:
        return self.size()

    def __str__(self) -> str:
        border = " ".join("X" * (self._width + 2))
        rows = [border]
        for row in self._cells:
            cells = " ".join(" " if unit is None else unit.get_symbol() for unit in row)
            rows.append(f"X {cells} X")
        rows.append(border)
        return "\n".join(rows)
