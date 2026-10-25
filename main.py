from game.units.cataphract import Cataphract
from game.units.heavy_archer import HeavyArcher
from game.units.horse_archer import HorseArcher
from game.units.light_archer import LightArcher
from game.units.spearman import Spearman
from game.units.swordsman import Swordsman


def show_units() -> None:
    print("=== Все виды юнитов ===")
    units = [
        Swordsman(0, 0),
        Spearman(1, 0),
        LightArcher(2, 0),
        HeavyArcher(3, 0),
        Cataphract(4, 0),
        HorseArcher(5, 0),
    ]
    for unit in units:
        print(f"{unit.get_category():<8} | {unit}")
    print()


def show_battle() -> None:
    print("=== Бой ===")
    swordsman = Swordsman(2, 2)
    spearman = Spearman(3, 2)
    archer = LightArcher(7, 2)

    damage = swordsman.hit(spearman)
    print(f"{swordsman.get_type()} бьёт {spearman.get_type()}: урон {damage}")
    damage = archer.hit(swordsman)
    print(f"{archer.get_type()} стреляет в {swordsman.get_type()}: урон {damage}")
    print(swordsman)
    print(spearman)

    try:
        swordsman.hit(archer)
    except ValueError as error:
        print(f"Ошибка: {error}")
    print()


def show_movement() -> None:
    print("=== Перемещение ===")
    cataphract = Cataphract(0, 0)
    cataphract.move_to(4, 3)
    print(f"После хода: {cataphract}")
    try:
        cataphract.move_to(10, 3)
    except ValueError as error:
        print(f"Ошибка: {error}")
    print()


def show_clone() -> None:
    print("=== Клонирование ===")
    original = HeavyArcher(1, 1)
    copy = original.clone()
    copy.take_damage(50)
    copy.move_to(2, 2)
    print(f"Оригинал: {original}")
    print(f"Копия:    {copy}")
    print(f"Здоровье общее: {original.health is copy.health}")
    print()


def main() -> None:
    show_units()
    show_battle()
    show_movement()
    show_clone()


if __name__ == "__main__":
    main()
