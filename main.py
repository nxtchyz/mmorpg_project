from game.factories.archer_factory import ArcherFactory
from game.factories.cavalry_factory import CavalryFactory
from game.factories.infantry_factory import InfantryFactory
from game.factories.unit_factory import UnitFactory
from game.field.game_field import GameField
from game.units.unit_kind import UnitKind

infantry_factory = InfantryFactory()
archer_factory = ArcherFactory()
cavalry_factory = CavalryFactory()
factories: list[UnitFactory] = [infantry_factory, archer_factory, cavalry_factory]


def show_factories() -> None:
    print("=== Фабрики юнитов ===")
    for factory in factories:
        print(type(factory).__name__)
        for kind in factory.supported_kinds():
            unit = factory.create_unit(kind)
            print(f"  {unit.get_category():<8} | {unit}")
    try:
        infantry_factory.create_unit(UnitKind.CATAPHRACT)
    except ValueError as error:
        print(f"Ошибка: {error}")
    print()


def show_battle() -> None:
    print("=== Бой ===")
    swordsman = infantry_factory.create_unit(UnitKind.SWORDSMAN, 2, 2)
    spearman = infantry_factory.create_unit(UnitKind.SPEARMAN, 3, 2)
    archer = archer_factory.create_unit(UnitKind.LIGHT_ARCHER, 7, 2)

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
    cataphract = cavalry_factory.create_unit(UnitKind.CATAPHRACT)
    cataphract.move_to(4, 3)
    print(f"После хода: {cataphract}")
    try:
        cataphract.move_to(10, 3)
    except ValueError as error:
        print(f"Ошибка: {error}")
    print()


def show_clone() -> None:
    print("=== Клонирование ===")
    original = archer_factory.create_unit(UnitKind.HEAVY_ARCHER, 1, 1)
    copy = original.clone()
    copy.take_damage(50)
    copy.move_to(2, 2)
    print(f"Оригинал: {original}")
    print(f"Копия:    {copy}")
    print(f"Здоровье общее: {original.health is copy.health}")
    print()


def show_field_population() -> None:
    print("=== Наполнение поля через фабрики ===")
    field = GameField(10, 8, 6)
    field.populate(infantry_factory, UnitKind.SWORDSMAN, [(1, 1), (2, 1)])
    field.populate(archer_factory, UnitKind.LIGHT_ARCHER, [(1, 6)])
    field.populate(archer_factory, UnitKind.HEAVY_ARCHER, [(2, 6)])
    field.populate(cavalry_factory, UnitKind.HORSE_ARCHER, [(8, 3), (8, 4)])
    print(f"Юнитов на поле: {field.size()} из {field.max_units}")
    print(f"На клетке (8, 3): {field.get_unit(8, 3)}")
    print(f"На клетке (5, 5): {field.get_unit(5, 5)}")

    try:
        field.populate(cavalry_factory, UnitKind.SPEARMAN, [(5, 5)])
    except ValueError as error:
        print(f"Ошибка: {error}")
    try:
        field.populate(cavalry_factory, UnitKind.CATAPHRACT, [(5, 5)])
    except OverflowError as error:
        print(f"Ошибка: {error}")
    print()


def main() -> None:
    show_factories()
    show_battle()
    show_movement()
    show_clone()
    show_field_population()


if __name__ == "__main__":
    main()
