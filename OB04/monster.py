"""
Модуль с классом монстра.
"""


class Monster:
    """Класс, представляющий монстра."""
    
    def __init__(self, name: str, health: int = 100):
        """
        Инициализация монстра.
        
        Args:
            name: Имя монстра
            health: Здоровье монстра
        """
        self.name = name
        self.health = health
        self.is_alive = True
    
    def take_damage(self, damage: int = 100) -> None:
        """
        Получить урон.
        
        Args:
            damage: Количество урона
        """
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False
            print(f"{self.name} побежден!")
        else:
            print(f"{self.name} получил урон! Осталось здоровья: {self.health}")
