"""
Модуль с классом бойца.
"""
from weapon import Weapon


class Fighter:
    """Класс, представляющий бойца."""
    
    def __init__(self, name: str):
        """
        Инициализация бойца.
        
        Args:
            name: Имя бойца
        """
        self.name = name
        self.weapon: Weapon = None
    
    def change_weapon(self, weapon: Weapon) -> None:
        """
        Изменить оружие бойца.
        
        Args:
            weapon: Объект класса Weapon
        """
        self.weapon = weapon
        print(f"{self.name} выбирает {weapon.__class__.__name__.lower()}.")
    
    def attack(self) -> str:
        """
        Выполнить атаку текущим оружием.
        
        Returns:
            str: Результат атаки
        """
        if self.weapon is None:
            return f"{self.name} не вооружен!"
        return self.weapon.attack()
