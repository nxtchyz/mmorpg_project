from abc import ABC, abstractmethod

from game.attributes.armor import Armor
from game.attributes.attack import Attack
from game.attributes.health import Health


class Unit(ABC):
    def __init__(self, health: Health, armor: Armor, attack: Attack, x: int = 0, y: int = 0) -> None:
        self._health = health
        self._armor = armor
        self._attack = attack
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
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def position(self) -> tuple[int, int]:
        return self._x, self._y

    def move_to(self, x: int, y: int) -> None:
        raise NotImplementedError

    def is_alive(self) -> bool:
        raise NotImplementedError

    def take_damage(self, damage: int) -> int:
        raise NotImplementedError

    def hit(self, target: "Unit") -> int:
        raise NotImplementedError

    @abstractmethod
    def get_type(self) -> str:
        ...

    @abstractmethod
    def get_symbol(self) -> str:
        ...

    @abstractmethod
    def clone(self) -> "Unit":
        ...
