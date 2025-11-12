# assets.py - Ініціалізація Pygame, завантаження шрифтів, зображень та музики

import pygame
import os
from config import WIDTH, HEIGHT, BLACK, CRACK_BLUE, BONE_WHITE

# Ініціалізація Pygame та мікшера
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Dying Light of Magic")

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # Усі напрямки руху
        self.images = {
            "up": [],
            "down": [],
            "left": [],
            "right": []
        }

        # Завантаження кадрів із папки images
        for direction in self.images.keys():
            for i in range(1, 4):  # 3 кадри на напрямок
                path = os.path.join("images", f"walk_{direction}_{i}.png")
                image = pygame.image.load(path).convert_alpha()
                image.set_colorkey((255, 255, 255))  # прибрати білий фон
                scaled = pygame.transform.scale(image, (64, 64))  # розмір під себе
                self.images[direction].append(scaled)

        # Початковий стан
        self.direction = "down"
        self.image_index = 0
        self.image = self.images[self.direction][self.image_index]
        self.rect = self.image.get_rect(center=pos)
        self.speed = 3
        self.animation_speed = 0.15

    def update(self):
        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        # Керування
        if keys[pygame.K_w]:
            self.direction = "up"
            dy = -self.speed
        elif keys[pygame.K_s]:
            self.direction = "down"
            dy = self.speed
        elif keys[pygame.K_a]:
            self.direction = "left"
            dx = -self.speed
        elif keys[pygame.K_d]:
            self.direction = "right"
            dx = self.speed

        # Рух
        self.rect.x += dx
        self.rect.y += dy

        # Анімація
        if dx != 0 or dy != 0:
            self.image_index += self.animation_speed
            if self.image_index >= len(self.images[self.direction]):
                self.image_index = 0
            self.image = self.images[self.direction][int(self.image_index)]
        else:
            # Стоїть — перший кадр
            self.image_index = 0
            self.image = self.images[self.direction][0]

# Шрифти
try:
    # ОНОВЛЕНО: Шлях до шрифту
    title_font = pygame.font.Font("fonts/CinzelDecorative-Bold.ttf", 80)
    menu_font = pygame.font.Font(None, 50)
    map_font = pygame.font.Font(None, 24)
except:
    # Запасний варіант, якщо шрифт не знайдено
    title_font = pygame.font.Font(None, 80)
    menu_font = pygame.font.Font(None, 50)
    map_font = pygame.font.Font(None, 24)

# Завантаження статичних ресурсів
try:
    # ОНОВЛЕНО: Шлях до фонового зображення
    background = pygame.transform.scale(pygame.image.load("images/fon.jpg"), (WIDTH, HEIGHT))
except:
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(BLACK)

try:
    # ОНОВЛЕНО: Шлях до зображення мапи
    world_map = pygame.image.load("images/map.jpg").convert()
except:
    world_map = pygame.Surface((2000, 2000))
    world_map.fill((30, 30, 40))

# Налаштування музики
try:
    # ОНОВЛЕНО: Шлях до музичного файлу
    pygame.mixer.music.load("music/bog_creatures_on_the_move.mp3")
    pygame.mixer.music.set_volume(0.5)
    _MUSIC_STATE = True # Прихована змінна стану
    pygame.mixer.music.play(-1)
except:
    _MUSIC_STATE = False
    
def get_music_state():
    """Повертає поточний стан музики (ON/OFF)."""
    return _MUSIC_STATE

def toggle_music():
    """Перемикає стан музики."""
    global _MUSIC_STATE
    _MUSIC_STATE = not _MUSIC_STATE
    if _MUSIC_STATE:
        try:
            # Спроба unpause, якщо вона була на паузі, або запустити заново
            pygame.mixer.music.unpause()
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
        except pygame.error:
            pass
    else:
        pygame.mixer.music.pause()
    return _MUSIC_STATE