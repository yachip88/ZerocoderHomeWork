"""
Битва героев — Battle of Heroes
Консольная игра на Python с использованием ООП.
Игрок и компьютер управляют героями, которые по очереди атакуют друг друга.
"""

import random


class Hero:
    """Класс героя с именем, здоровьем и силой удара."""

    def __init__(self, name: str, health: int = 100, attack_power: int = 20):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def attack(self, other: "Hero") -> int:
        """Атакует другого героя. Возвращает нанесённый урон."""
        # Небольшой разброс урона: ±5
        damage = random.randint(
            max(1, self.attack_power - 5),
            self.attack_power + 5
        )
        other.health -= damage
        if other.health < 0:
            other.health = 0
        return damage

    def is_alive(self) -> bool:
        """Возвращает True, если герой жив (здоровье > 0)."""
        return self.health > 0

    def __str__(self) -> str:
        return f"{self.name} [HP: {self.health}]"


class Game:
    """Класс игры, управляющий процессом боя."""

    def __init__(self, player: Hero, computer: Hero):
        self.player = player
        self.computer = computer
        self.round_num = 0

    def start(self):
        """Запускает игру: чередует ходы, пока один герой не погибнет."""
        print("=" * 50)
        print("⚔️  БИТВА ГЕРОЕВ  ⚔️")
        print("=" * 50)
        print(f"\n🦸 Игрок:    {self.player}")
        print(f"🤖 Компьютер: {self.computer}")
        print("-" * 50)

        while self.player.is_alive() and self.computer.is_alive():
            self.round_num += 1
            print(f"\n--- Раунд {self.round_num} ---")

            # Ход игрока
            damage = self.player.attack(self.computer)
            print(f"🗡️  {self.player.name} атакует {self.computer.name} "
                  f"и наносит {damage} урона!")
            print(f"   {self.computer}")

            if not self.computer.is_alive():
                break

            # Ход компьютера
            damage = self.computer.attack(self.player)
            print(f"🗡️  {self.computer.name} атакует {self.player.name} "
                  f"и наносит {damage} урона!")
            print(f"   {self.player}")

        # Объявление победителя
        print("\n" + "=" * 50)
        if self.player.is_alive():
            print(f"🏆 Победил {self.player.name}! Поздравляем!")
        else:
            print(f"💀 Победил {self.computer.name}! Попробуйте ещё раз!")
        print("=" * 50)


# ─── Точка входа ────────────────────────────────────────────
if __name__ == "__main__":
    player_name = input("Введите имя вашего героя: ").strip()
    if not player_name:
        player_name = "Герой"

    player = Hero(name=player_name)
    computer = Hero(name="Дракон")

    game = Game(player, computer)
    game.start()
