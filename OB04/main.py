"""
Главный модуль для демонстрации боевой системы с применением принципа Open/Closed.
"""
from fighter import Fighter
from monster import Monster
from weapon import Sword, Bow, Axe, Spear


def battle(fighter: Fighter, monster: Monster) -> None:
    """
    Провести бой между бойцом и монстром.
    
    Args:
        fighter: Объект бойца
        monster: Объект монстра
    """
    print(fighter.attack())
    monster.take_damage()
    print()


def main():
    """Главная функция для демонстрации работы программы."""
    print("=== Демонстрация принципа Open/Closed ===\n")
    
    # Создаем бойца
    fighter = Fighter("Воин")
    
    # Демонстрация с разными типами оружия
    weapons = [Sword(), Bow(), Axe(), Spear()]
    
    for weapon in weapons:
        # Создаем нового монстра для каждого боя
        monster = Monster("Монстр")
        
        # Меняем оружие
        fighter.change_weapon(weapon)
        
        # Проводим бой
        battle(fighter, monster)
    
    print("=== Демонстрация завершена ===")
    print("\nПринцип Open/Closed соблюден:")
    print("- Классы открыты для расширения (можно легко добавить новые типы оружия)")
    print("- Классы закрыты для модификации (не нужно изменять Fighter или Monster)")


if __name__ == "__main__":
    main()
