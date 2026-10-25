from abc import ABC, abstractmethod

from game.attributes.armor import Armor
from game.attributes.attack import Attack
from game.attributes.health import Health


class Unit(ABC):
    def __init__(
        self,
        health: Health,
        armor: Armor,
        attack: Attack,
        speed: int,
        attack_range: int,
        x: int = 0,
        y: int = 0,
    ) -> None:
        if speed <= 0:
            raise ValueError("Скорость юнита должна быть положительной")
        if attack_range <= 0:
            raise ValueError("Дальность атаки должна быть положительной")
        self._check_coordinates(x, y)
        self._health = health
        self._armor = armor
        self._attack = attack
        self._speed = speed
        self._attack_range = attack_range
        self._x = x
        self._y = y

    @property
    def health(self) -> Health:
        return self._health

    @property
    def armor(self) -> Armor:
        return self._armor

    @property
    def attack(self) -> Attack:
        return self._attack

    @property
    def speed(self) -> int:
        return self._speed

    @property
    def attack_range(self) -> int:
        return self._attack_range

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def position(self) -> tuple[int, int]:
        return self._x, self._y

    def distance_to(self, x: int, y: int) -> int:
        return max(abs(self._x - x), abs(self._y - y))

    def can_reach(self, x: int, y: int) -> bool:
        return self.distance_to(x, y) <= self._speed

    def move_to(self, x: int, y: int) -> None:
        self._check_coordinates(x, y)
        if not self.is_alive():
            raise ValueError(f"{self.get_type()} погиб и не может перемещаться")
        if not self.can_reach(x, y):
            raise ValueError(f"{self.get_type()} не может пройти больше {self._speed} клеток за ход")
        self._x = x
        self._y = y

    def is_alive(self) -> bool:
        return not self._health.is_zero()

    def take_damage(self, damage: int) -> int:
        if damage < 0:
            raise ValueError("Урон не может быть отрицательным")
        return self._health.decrease(damage)

    def hit(self, target: "Unit") -> int:
        if target is self:
            raise ValueError("Юнит не может атаковать сам себя")
        if not self.is_alive():
            raise ValueError(f"{self.get_type()} погиб и не может атаковать")
        if not target.is_alive():
            raise ValueError(f"{target.get_type()} уже погиб")
        if self.distance_to(target.x, target.y) > self._attack_range:
            raise ValueError(f"{target.get_type()} вне дальности атаки")
        damage = self._attack.calculate_damage(target.armor)
        return target.take_damage(damage)

    @staticmethod
    def _check_coordinates(x: int, y: int) -> None:
        if x < 0 or y < 0:
            raise ValueError("Координаты юнита не могут быть отрицательными")

    @abstractmethod
    def get_category(self) -> str:
        ...

    @abstractmethod
    def get_type(self) -> str:
        ...

    @abstractmethod
    def get_symbol(self) -> str:
        ...

    @abstractmethod
    def clone(self) -> "Unit":
        ...

    def __str__(self) -> str:
        return (
            f"{self.get_type()} [{self.get_symbol()}] ({self._x}, {self._y}) "
            f"HP {self._health.value}/{self._health.max_value} "
            f"ARM {self._armor.value} ATK {self._attack.value}"
        )
