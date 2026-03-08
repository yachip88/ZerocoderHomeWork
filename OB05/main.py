"""
Космический шутер — Space Defender
Игра на Pygame с использованием ООП.
Управление стрелками, автострельба, падающие объекты,
подсчёт очков, таймер, топ-3 игроков.
"""

import pygame
import sys
import random
import math
import json
import os
import time as time_module

# ─── Константы ──────────────────────────────────────────────
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 220, 50)
CYAN = (0, 255, 255)
RED = (255, 60, 60)
ORANGE = (255, 140, 40)
GREEN = (80, 255, 120)
DARK_BLUE = (10, 10, 40)
LIGHT_BLUE = (100, 180, 255)
GREY = (180, 180, 180)
DARK_GREY = (80, 80, 80)
PURPLE = (180, 80, 255)

SCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "top_scores.json")

SHOOT_INTERVAL = 250          # мс между выстрелами
OBSTACLE_BASE_INTERVAL = 1200  # мс, уменьшается со временем
OBSTACLE_MIN_INTERVAL = 300
PLAYER_SPEED = 6


# ─── Класс Star (фоновые звёзды) ───────────────────────────
class Star:
    """Фоновая звезда с параллакс-эффектом."""

    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.layer = random.choice([1, 2, 3])  # 1=далёкая, 3=близкая
        self.speed = self.layer * 0.4
        self.size = self.layer
        brightness = 80 + self.layer * 50
        self.color = (min(255, brightness), min(255, brightness), min(255, brightness + 30))

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)


# ─── Класс Particle (частица взрыва) ───────────────────────
class Particle:
    """Одна частица эффекта взрыва."""

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 5)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.randint(15, 35)
        self.max_life = self.life
        self.color = color
        self.size = random.uniform(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05  # гравитация
        self.life -= 1

    def draw(self, surface):
        alpha_ratio = self.life / self.max_life
        r = min(255, int(self.color[0] * alpha_ratio + 255 * (1 - alpha_ratio)))
        g = min(255, int(self.color[1] * alpha_ratio))
        b = min(255, int(self.color[2] * alpha_ratio))
        size = max(1, int(self.size * alpha_ratio))
        pygame.draw.circle(surface, (r, g, b), (int(self.x), int(self.y)), size)

    @property
    def alive(self):
        return self.life > 0


# ─── Класс Explosion (взрыв) ───────────────────────────────
class Explosion:
    """Взрыв, состоящий из множества частиц."""

    def __init__(self, x, y, color=ORANGE, count=25):
        self.particles = [Particle(x, y, color) for _ in range(count)]

    def update(self):
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.alive]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)

    @property
    def alive(self):
        return len(self.particles) > 0


# ─── Класс Bullet (пуля) ───────────────────────────────────
class Bullet:
    """Пуля, выпущенная игроком вверх."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 8
        self.width = 3
        self.height = 14
        self.color = CYAN
        self.glow_color = (0, 150, 255)

    def update(self):
        self.y -= self.speed

    def draw(self, surface):
        # свечение
        glow_surf = pygame.Surface((self.width + 6, self.height + 6), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*self.glow_color, 60),
                         (0, 0, self.width + 6, self.height + 6), border_radius=3)
        surface.blit(glow_surf, (int(self.x - self.width // 2 - 3),
                                  int(self.y - self.height // 2 - 3)))
        # пуля
        pygame.draw.rect(surface, self.color,
                         (int(self.x - self.width // 2), int(self.y - self.height // 2),
                          self.width, self.height), border_radius=2)

    def get_rect(self):
        return pygame.Rect(int(self.x - self.width // 2), int(self.y - self.height // 2),
                           self.width, self.height)

    @property
    def off_screen(self):
        return self.y < -20


# ─── Класс Player (корабль игрока) ─────────────────────────
class Player:
    """Космический корабль игрока."""

    def __init__(self):
        self.width = 48
        self.height = 52
        self.x = WIDTH // 2
        self.y = HEIGHT - 80
        self.speed = PLAYER_SPEED
        self.last_shot_time = 0
        self.engine_frame = 0

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.x - self.width // 2 > 5:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.width // 2 < WIDTH - 5:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y - self.height // 2 > 5:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y + self.height // 2 < HEIGHT - 5:
            self.y += self.speed
        self.engine_frame = (self.engine_frame + 1) % 20

    def try_shoot(self, current_time):
        """Возвращает Bullet или None."""
        if current_time - self.last_shot_time >= SHOOT_INTERVAL:
            self.last_shot_time = current_time
            return Bullet(self.x, self.y - self.height // 2 - 5)
        return None

    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        hw, hh = self.width // 2, self.height // 2

        # Корпус корабля (треугольник + крылья)
        body_points = [
            (cx, cy - hh),            # нос
            (cx - 8, cy + 5),         # лев. борт
            (cx - hw, cy + hh - 5),   # лев. крыло
            (cx - 10, cy + hh),       # лев. нижн.
            (cx + 10, cy + hh),       # прав. нижн.
            (cx + hw, cy + hh - 5),   # прав. крыло
            (cx + 8, cy + 5),         # прав. борт
        ]
        pygame.draw.polygon(surface, (60, 130, 220), body_points)
        pygame.draw.polygon(surface, (100, 180, 255), body_points, 2)

        # Кабина (маленький эллипс)
        pygame.draw.ellipse(surface, (150, 220, 255),
                            (cx - 6, cy - 12, 12, 16))
        pygame.draw.ellipse(surface, (200, 240, 255),
                            (cx - 4, cy - 9, 8, 10))

        # Двигатель (пламя, меняющееся по кадрам)
        flame_len = 12 + (self.engine_frame % 10)
        flame_points = [
            (cx - 7, cy + hh),
            (cx, cy + hh + flame_len),
            (cx + 7, cy + hh),
        ]
        flame_color = ORANGE if self.engine_frame < 10 else YELLOW
        pygame.draw.polygon(surface, flame_color, flame_points)
        # внутреннее пламя
        inner_len = 6 + (self.engine_frame % 6)
        inner_points = [
            (cx - 3, cy + hh),
            (cx, cy + hh + inner_len),
            (cx + 3, cy + hh),
        ]
        pygame.draw.polygon(surface, YELLOW, inner_points)

    def get_rect(self):
        return pygame.Rect(int(self.x - self.width // 2), int(self.y - self.height // 2),
                           self.width, self.height)


# ─── Класс Obstacle (падающий объект) ──────────────────────
class Obstacle:
    """Падающий космический объект (астероид, метеорит, спутник)."""

    TYPES = [
        {"name": "asteroid",  "color": (160, 130, 100), "outline": (200, 170, 130), "points": 10,  "size": (22, 32), "speed": (1.5, 3.0)},
        {"name": "meteorite", "color": (200, 80, 50),   "outline": (255, 120, 80),  "points": 20,  "size": (16, 24), "speed": (2.5, 4.5)},
        {"name": "satellite", "color": (130, 130, 160),  "outline": (180, 180, 220), "points": 30,  "size": (18, 26), "speed": (1.0, 2.5)},
    ]

    def __init__(self):
        t = random.choice(self.TYPES)
        self.name = t["name"]
        self.color = t["color"]
        self.outline = t["outline"]
        self.points = t["points"]
        self.radius = random.randint(t["size"][0], t["size"][1])
        self.x = random.randint(self.radius + 10, WIDTH - self.radius - 10)
        self.y = -self.radius * 2
        self.speed = random.uniform(t["speed"][0], t["speed"][1])
        self.rotation = random.uniform(0, 360)
        self.rot_speed = random.uniform(-3, 3)
        # Генерируем неровную форму для астероида
        self.shape_offsets = [random.uniform(0.7, 1.0) for _ in range(10)]

    def update(self):
        self.y += self.speed
        self.rotation += self.rot_speed

    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        r = self.radius

        if self.name == "satellite":
            # Спутник: прямоугольное тело + солнечные панели
            body_w, body_h = r, int(r * 0.6)
            pygame.draw.rect(surface, self.color,
                             (cx - body_w // 2, cy - body_h // 2, body_w, body_h))
            pygame.draw.rect(surface, self.outline,
                             (cx - body_w // 2, cy - body_h // 2, body_w, body_h), 2)
            # Панели
            panel_w = int(r * 0.8)
            pygame.draw.rect(surface, (60, 80, 160),
                             (cx - body_w // 2 - panel_w, cy - 4, panel_w, 8))
            pygame.draw.rect(surface, (60, 80, 160),
                             (cx + body_w // 2, cy - 4, panel_w, 8))
            pygame.draw.rect(surface, (100, 130, 220),
                             (cx - body_w // 2 - panel_w, cy - 4, panel_w, 8), 1)
            pygame.draw.rect(surface, (100, 130, 220),
                             (cx + body_w // 2, cy - 4, panel_w, 8), 1)
            # Антенна
            pygame.draw.line(surface, GREY, (cx, cy - body_h // 2), (cx, cy - body_h // 2 - 8), 1)
            pygame.draw.circle(surface, RED, (cx, cy - body_h // 2 - 8), 2)
        else:
            # Астероид/метеорит: неровный многоугольник
            num_pts = len(self.shape_offsets)
            pts = []
            for i in range(num_pts):
                angle = math.radians(self.rotation + i * (360 / num_pts))
                offset = self.shape_offsets[i]
                px = cx + int(math.cos(angle) * r * offset)
                py = cy + int(math.sin(angle) * r * offset)
                pts.append((px, py))
            pygame.draw.polygon(surface, self.color, pts)
            pygame.draw.polygon(surface, self.outline, pts, 2)
            # Кратеры
            if self.name == "asteroid":
                cr_x = cx + int(r * 0.2)
                cr_y = cy - int(r * 0.15)
                cr_r = max(2, r // 5)
                darker = (max(0, self.color[0] - 40), max(0, self.color[1] - 40), max(0, self.color[2] - 40))
                pygame.draw.circle(surface, darker, (cr_x, cr_y), cr_r)
            elif self.name == "meteorite":
                # Огненный хвост
                for i in range(3):
                    tail_y = cy - r - i * 5
                    tw = max(1, r // 3 - i * 2)
                    alpha_color = (255, 100 + i * 40, 0)
                    pygame.draw.circle(surface, alpha_color, (cx + random.randint(-3, 3), tail_y), tw)

    def get_rect(self):
        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius),
                           self.radius * 2, self.radius * 2)

    @property
    def off_screen(self):
        return self.y > HEIGHT + self.radius * 2


# ─── Класс ScoreBoard (лидерборд) ─────────────────────────
class ScoreBoard:
    """Управление топ-3 рекордов (хранение в JSON файле)."""

    def __init__(self, filepath=SCORE_FILE):
        self.filepath = filepath
        self.scores = self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return data[:3]
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.scores, f, ensure_ascii=False, indent=2)

    def add_score(self, name, score, play_time):
        """Добавляет результат. Возвращает (place, is_record)."""
        entry = {"name": name, "score": score, "time": play_time}
        self.scores.append(entry)
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.scores = self.scores[:3]
        self._save()

        # Определяем место
        for i, s in enumerate(self.scores):
            if s["name"] == name and s["score"] == score and s["time"] == play_time:
                is_record = (i == 0)
                return i + 1, is_record
        return None, False

    def get_top(self):
        return self.scores


# ─── Класс Game (главный класс игры) ──────────────────────
class Game:
    """Главный класс, управляющий всеми состояниями и игровым циклом."""

    STATE_NAME_INPUT = "name_input"
    STATE_PLAYING = "playing"
    STATE_GAME_OVER = "game_over"

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("🚀 Space Defender — Космический Защитник")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont("Arial", 48, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 28)
        self.font_small = pygame.font.SysFont("Arial", 20)
        self.font_tiny = pygame.font.SysFont("Arial", 16)

        self.scoreboard = ScoreBoard()
        self.stars = [Star() for _ in range(120)]

        self.state = self.STATE_NAME_INPUT
        self.player_name = ""
        self.cursor_blink = 0

        # Игровые объекты
        self.player = None
        self.bullets = []
        self.obstacles = []
        self.explosions = []
        self.score = 0
        self.start_time = 0
        self.elapsed_time = 0
        self.last_obstacle_time = 0
        self.obstacle_interval = OBSTACLE_BASE_INTERVAL

        # Результат
        self.result_place = None
        self.result_is_record = False

    def run(self):
        """Главный цикл."""
        running = True
        while running:
            dt = self.clock.tick(FPS)
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            # Обновление фоновых звёзд
            for star in self.stars:
                star.update()

            if self.state == self.STATE_NAME_INPUT:
                self._handle_name_input(events)
                self._draw_name_input()
            elif self.state == self.STATE_PLAYING:
                self._handle_playing(events)
                self._update_playing()
                self._draw_playing()
            elif self.state == self.STATE_GAME_OVER:
                self._handle_game_over(events)
                self._draw_game_over()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    # ──── NAME INPUT ────────────────────────────────────────
    def _handle_name_input(self, events):
        self.cursor_blink = (self.cursor_blink + 1) % 60
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(self.player_name.strip()) > 0:
                    self._start_game()
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif len(self.player_name) < 15 and event.unicode.isprintable() and event.unicode != '':
                    self.player_name += event.unicode

    def _draw_name_input(self):
        self.screen.fill(DARK_BLUE)
        self._draw_stars()

        # Заголовок
        title = self.font_large.render("SPACE DEFENDER", True, CYAN)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        subtitle = self.font_small.render("🚀  Космический Защитник  🚀", True, LIGHT_BLUE)
        self.screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 160))

        # Инструкции
        instr_lines = [
            "Управление: ← → ↑ ↓",
            "Стрельба — автоматическая",
            "Уничтожай объекты и набирай очки!",
        ]
        for i, line in enumerate(instr_lines):
            txt = self.font_small.render(line, True, GREY)
            self.screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 220 + i * 30))

        # Поле ввода имени
        prompt = self.font_medium.render("Введите ваше имя:", True, WHITE)
        self.screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 340))

        # Рамка ввода
        input_rect = pygame.Rect(WIDTH // 2 - 150, 385, 300, 45)
        pygame.draw.rect(self.screen, (30, 30, 80), input_rect, border_radius=8)
        pygame.draw.rect(self.screen, CYAN, input_rect, 2, border_radius=8)

        cursor = "│" if self.cursor_blink < 30 else ""
        name_text = self.font_medium.render(self.player_name + cursor, True, WHITE)
        self.screen.blit(name_text, (input_rect.x + 12, input_rect.y + 8))

        hint = self.font_tiny.render("Нажмите ENTER чтобы начать", True, DARK_GREY)
        self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 445))

        # Топ рекордов
        top = self.scoreboard.get_top()
        if top:
            top_title = self.font_small.render("🏆 Топ-3 игроков:", True, YELLOW)
            self.screen.blit(top_title, (WIDTH // 2 - top_title.get_width() // 2, 490))
            medals = ["🥇", "🥈", "🥉"]
            for i, s in enumerate(top):
                line = f"{medals[i]} {s['name']} — {s['score']} очков ({s['time']}с)"
                color = [YELLOW, (210, 210, 210), (205, 127, 50)][i]
                txt = self.font_small.render(line, True, color)
                self.screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 520 + i * 28))

    # ──── PLAYING ───────────────────────────────────────────
    def _start_game(self):
        self.state = self.STATE_PLAYING
        self.player = Player()
        self.bullets = []
        self.obstacles = []
        self.explosions = []
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.last_obstacle_time = self.start_time
        self.obstacle_interval = OBSTACLE_BASE_INTERVAL

    def _handle_playing(self, events):
        pass  # Все управление через keys в update

    def _update_playing(self):
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        self.elapsed_time = (now - self.start_time) // 1000

        # Обновление игрока
        self.player.update(keys)

        # Автострельба
        bullet = self.player.try_shoot(now)
        if bullet:
            self.bullets.append(bullet)

        # Обновление пуль
        for b in self.bullets:
            b.update()
        self.bullets = [b for b in self.bullets if not b.off_screen]

        # Спавн объектов (нарастающая сложность)
        self.obstacle_interval = max(OBSTACLE_MIN_INTERVAL,
                                     OBSTACLE_BASE_INTERVAL - self.elapsed_time * 10)
        if now - self.last_obstacle_time >= self.obstacle_interval:
            self.obstacles.append(Obstacle())
            self.last_obstacle_time = now

        # Обновление объектов
        for o in self.obstacles:
            o.update()

        # Обновление взрывов
        for e in self.explosions:
            e.update()
        self.explosions = [e for e in self.explosions if e.alive]

        # Проверка столкновений: пули → объекты
        new_obstacles = []
        for o in self.obstacles:
            hit = False
            o_rect = o.get_rect()
            for b in self.bullets[:]:
                if o_rect.colliderect(b.get_rect()):
                    hit = True
                    self.bullets.remove(b)
                    self.score += o.points
                    self.explosions.append(Explosion(int(o.x), int(o.y), o.outline, 20))
                    break
            if not hit:
                new_obstacles.append(o)
        self.obstacles = new_obstacles

        # Удаление вышедших за экран
        self.obstacles = [o for o in self.obstacles if not o.off_screen]

        # Столкновение объекта с игроком
        player_rect = self.player.get_rect().inflate(-12, -12)  # чуть уменьшенный хитбокс
        for o in self.obstacles:
            if player_rect.colliderect(o.get_rect()):
                self.explosions.append(Explosion(int(self.player.x), int(self.player.y), RED, 40))
                self._end_game()
                return

    def _end_game(self):
        self.state = self.STATE_GAME_OVER
        play_time = self.elapsed_time
        place, is_record = self.scoreboard.add_score(
            self.player_name.strip(), self.score, play_time
        )
        self.result_place = place
        self.result_is_record = is_record

    def _draw_playing(self):
        self.screen.fill(DARK_BLUE)
        self._draw_stars()

        # Объекты
        for o in self.obstacles:
            o.draw(self.screen)

        # Пули
        for b in self.bullets:
            b.draw(self.screen)

        # Игрок
        self.player.draw(self.screen)

        # Взрывы
        for e in self.explosions:
            e.draw(self.screen)

        # HUD: очки
        score_txt = self.font_medium.render(f"Очки: {self.score}", True, YELLOW)
        self.screen.blit(score_txt, (15, 10))

        # HUD: таймер
        time_txt = self.font_small.render(f"Время: {self.elapsed_time}с", True, LIGHT_BLUE)
        self.screen.blit(time_txt, (WIDTH - time_txt.get_width() - 15, 15))

        # HUD: имя
        name_txt = self.font_tiny.render(f"Пилот: {self.player_name}", True, GREY)
        self.screen.blit(name_txt, (15, 45))

    # ──── GAME OVER ─────────────────────────────────────────
    def _handle_game_over(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self._start_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_n:
                    self.state = self.STATE_NAME_INPUT
                    self.player_name = ""

    def _draw_game_over(self):
        self.screen.fill(DARK_BLUE)
        self._draw_stars()

        # Взрывы (доигрывают)
        for e in self.explosions:
            e.update()
            e.draw(self.screen)
        self.explosions = [e for e in self.explosions if e.alive]

        # Полупрозрачный оверлей
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # Заголовок
        go_text = self.font_large.render("GAME OVER", True, RED)
        self.screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, 100))

        # Результат
        score_txt = self.font_medium.render(f"Ваш счёт: {self.score}", True, WHITE)
        self.screen.blit(score_txt, (WIDTH // 2 - score_txt.get_width() // 2, 175))
        time_txt = self.font_small.render(f"Время: {self.elapsed_time}с", True, LIGHT_BLUE)
        self.screen.blit(time_txt, (WIDTH // 2 - time_txt.get_width() // 2, 215))

        # Рекорд?
        if self.result_is_record:
            rec_txt = self.font_medium.render("🎉 НОВЫЙ РЕКОРД! 🎉", True, YELLOW)
            self.screen.blit(rec_txt, (WIDTH // 2 - rec_txt.get_width() // 2, 255))
        elif self.result_place is not None:
            place_txt = self.font_small.render(f"Вы на {self.result_place} месте!", True, GREEN)
            self.screen.blit(place_txt, (WIDTH // 2 - place_txt.get_width() // 2, 260))

        # Топ-3
        top = self.scoreboard.get_top()
        if top:
            top_y = 310
            top_title = self.font_small.render("🏆 Топ-3 игроков:", True, YELLOW)
            self.screen.blit(top_title, (WIDTH // 2 - top_title.get_width() // 2, top_y))
            medals = ["🥇", "🥈", "🥉"]
            for i, s in enumerate(top):
                line = f"{medals[i]} {s['name']} — {s['score']} очков ({s['time']}с)"
                colors = [YELLOW, (210, 210, 210), (205, 127, 50)]
                txt = self.font_small.render(line, True, colors[i])
                self.screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, top_y + 30 + i * 28))

        # Подсказки
        hints = [
            "R — играть заново",
            "N — ввести другое имя",
            "Q — выйти",
        ]
        for i, h in enumerate(hints):
            txt = self.font_tiny.render(h, True, GREY)
            self.screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 460 + i * 24))

    # ──── Вспомогательные методы ────────────────────────────
    def _draw_stars(self):
        for star in self.stars:
            star.draw(self.screen)


# ─── Точка входа ────────────────────────────────────────────
if __name__ == "__main__":
    game = Game()
    game.run()
