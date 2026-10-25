from collections.abc import Iterable

from game.factories.unit_factory import UnitFactory
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
        return 0 <= x < self._width and 0 <= y < self._height

    def is_free(self, x: int, y: int) -> bool:
        return self.is_inside(x, y) and self._cells[y][x] is None

    def is_full(self) -> bool:
        return self._count >= self._max_units

    def add_unit(self, unit: Unit) -> None:
        x, y = unit.position
        if not self.is_inside(x, y):
            raise ValueError(f"Клетка ({x}, {y}) за пределами поля")
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
        raise NotImplementedError

    def get_unit(self, x: int, y: int) -> Unit | None:
        if not self.is_inside(x, y):
            raise ValueError(f"Клетка ({x}, {y}) за пределами поля")
        return self._cells[y][x]

    def move_unit(self, from_x: int, from_y: int, to_x: int, to_y: int) -> None:
        raise NotImplementedError

    def size(self) -> int:
        return self._count

    def empty(self) -> bool:
        return self._count == 0

    def clear(self) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        return self.size()
