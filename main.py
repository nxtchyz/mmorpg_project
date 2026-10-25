from copy import deepcopy

from game.attributes.attack import Attack
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


def title(text: str) -> None:
    print(f"\n=== {text} ===")


def build_field() -> GameField:
    field = GameField(12, 8, 10)
    field.populate(infantry_factory, UnitKind.SWORDSMAN, [(1, 2), (1, 4)])
    field.populate(infantry_factory, UnitKind.SPEARMAN, [(2, 3)])
    field.populate(archer_factory, UnitKind.LIGHT_ARCHER, [(0, 1), (0, 5)])
    field.populate(archer_factory, UnitKind.HEAVY_ARCHER, [(0, 3)])
    field.populate(cavalry_factory, UnitKind.CATAPHRACT, [(9, 2), (9, 5)])
    field.populate(cavalry_factory, UnitKind.HORSE_ARCHER, [(10, 3)])
    return field


def scenario_factories() -> None:
    title("Фабрики юнитов")
    for factory in factories:
        print(type(factory).__name__)
        for kind in factory.supported_kinds():
            unit = factory.create_unit(kind)
            print(f"  {unit.get_category():<8} | {unit.get_type():<15} [{unit.get_symbol()}]")
    try:
        infantry_factory.create_unit(UnitKind.CATAPHRACT)
    except ValueError as error:
        print(f"Ошибка: {error}")


def scenario_populate() -> None:
    title("1. Создание поля и наполнение через фабрики")
    field = build_field()
    print(field)
    print(f"Юнитов на поле: {field.size()} из {field.max_units}")

    field.populate(cavalry_factory, UnitKind.HORSE_ARCHER, [(11, 7)])
    print(f"Добавлен ещё один конный лучник, поле заполнено: {field.is_full()}")
    try:
        field.populate(infantry_factory, UnitKind.SWORDSMAN, [(5, 5)])
    except OverflowError as error:
        print(f"Ошибка: {error}")
    try:
        field.populate(archer_factory, UnitKind.CATAPHRACT, [(5, 5)])
    except ValueError as error:
        print(f"Ошибка: {error}")
    try:
        field.get_unit(20, 20)
    except IndexError as error:
        print(f"Ошибка: {error}")


def scenario_deep_copy() -> None:
    title("2. Глубокое копирование поля")
    original = build_field()
    duplicate = original.copy()

    duplicate.get_unit(1, 2).take_damage(100)
    duplicate.remove_unit(9, 5)
    duplicate.move_unit(9, 2, 6, 2)

    print("Оригинал:")
    print(original)
    print("Копия после изменений:")
    print(duplicate)
    print(f"Юнитов в оригинале: {original.size()}, в копии: {duplicate.size()}")
    print(f"Мечник (1, 2) в оригинале: {original.get_unit(1, 2).health.value} HP")
    print(f"Мечник (1, 2) в копии:     {duplicate.get_unit(1, 2).health.value} HP")
    print(f"Есть общие юниты: {any(a is b for a in original for b in duplicate)}")

    standard = deepcopy(original)
    print(f"copy.deepcopy тоже даёт независимую копию: {standard.get_unit(9, 2) is not original.get_unit(9, 2)}")


def scenario_move() -> None:
    title("3. Перемещение поля (передача владения)")
    source = build_field()
    first_unit = source.get_unit(0, 1)

    target = GameField.from_moved(source)
    print(f"from_moved: в новом поле {target.size()} юнитов, старое пустое: {source.empty()}")
    print(f"Юниты не копировались, а перешли: {target.get_unit(0, 1) is first_unit}")

    other = GameField(5, 5, 3)
    other.move_from(target)
    print(f"move_from: поле стало {other.width}x{other.height}, юнитов {other.size()}, источник пустой: {target.empty()}")

    snapshot = GameField(3, 3, 1)
    snapshot.assign(other)
    snapshot.remove_unit(0, 1)
    print(f"assign: у копии {snapshot.size()} юнитов, у исходного поля осталось {other.size()}")


def scenario_iteration() -> GameField:
    title("4. Обход итератором: массовое действие")
    field = build_field()
    volley = Attack(75)
    print(f"Залп по всему полю силой {volley.value}:")
    for unit in field:
        lost = unit.take_damage(volley.calculate_damage(unit.armor))
        position = f"({unit.x}, {unit.y})"
        print(f"  {unit.get_type():<15} {position:<8} -{lost:>2} HP, осталось {unit.health.value}")

    iterator = iter(field)
    alive = 0
    while iterator.has_next():
        if iterator.next().is_alive():
            alive += 1
    print(f"Выживших (подсчёт через has_next/next): {alive} из {field.size()}")
    return field


def scenario_remove_during_iteration(field: GameField) -> None:
    title("5. Удаление во время итерации")
    for unit in field:
        if not unit.is_alive():
            field.remove_unit(unit.x, unit.y)
            print(f"  Убран погибший: {unit.get_type()} ({unit.x}, {unit.y})")
    print(field)
    print(f"Осталось юнитов: {field.size()}")


def scenario_battle() -> None:
    title("6. Бой на поле")
    field = GameField(10, 5, 4)
    archer = field.populate(archer_factory, UnitKind.LIGHT_ARCHER, [(1, 2)])[0]
    cataphract = field.populate(cavalry_factory, UnitKind.CATAPHRACT, [(8, 2)])[0]
    print(field)

    turn = 1
    while archer.is_alive() and cataphract.is_alive():
        if archer.distance_to(cataphract.x, cataphract.y) <= archer.attack_range:
            print(f"Ход {turn}: {archer.get_type()} стреляет, урон {archer.hit(cataphract)}")
        if archer.distance_to(cataphract.x, cataphract.y) > cataphract.attack_range:
            to_x = max(archer.x + 1, cataphract.x - cataphract.speed)
            field.move_unit(cataphract.x, cataphract.y, to_x, cataphract.y)
            print(f"Ход {turn}: {cataphract.get_type()} скачет на ({cataphract.x}, {cataphract.y})")
        else:
            print(f"Ход {turn}: {cataphract.get_type()} атакует, урон {cataphract.hit(archer)}")
        turn += 1

    for unit in field:
        if not unit.is_alive():
            field.remove_unit(unit.x, unit.y)
    print(field)
    winner = next(iter(field))
    print(f"Победитель: {winner}")

    try:
        field.move_unit(winner.x, winner.y, 9, 4)
    except ValueError as error:
        print(f"Ошибка: {error}")


def main() -> None:
    scenario_factories()
    scenario_populate()
    scenario_deep_copy()
    scenario_move()
    field = scenario_iteration()
    scenario_remove_during_iteration(field)
    scenario_battle()


if __name__ == "__main__":
    main()
