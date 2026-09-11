import pygame
import random

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Игра Тир")

target_width = 80
target_height = 80
target_x = random.randint(0, SCREEN_WIDTH - target_width)
target_y = random.randint(0, SCREEN_HEIGHT - target_height)
color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
hits = 0
font = pygame.font.SysFont(None, 36)

running = True
clock = pygame.time.Clock()
while running:
    screen.fill(color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if target_x < mouse_x < target_x + target_width and target_y < mouse_y < target_y + target_height:
                target_x = random.randint(0, SCREEN_WIDTH - target_width)
                target_y = random.randint(0, SCREEN_HEIGHT - target_height)
                hits += 1
    pygame.draw.circle(
        screen,
        (220, 40, 40),
        (target_x + target_width // 2, target_y + target_height // 2),
        target_width // 2,
    )
    pygame.draw.circle(
        screen,
        (240, 240, 240),
        (target_x + target_width // 2, target_y + target_height // 2),
        target_width // 4,
    )
    text = font.render(f"Попадания: {hits}", True, (255, 255, 255))
    screen.blit(text, (16, 16))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
