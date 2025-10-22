# assets.py - Ініціалізація Pygame, завантаження шрифтів, зображень та музики

import pygame
import os
from config import WIDTH, HEIGHT, BLACK, CRACK_BLUE, BONE_WHITE

# Ініціалізація Pygame та мікшера
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Dying Light of Magic")

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

# Гравець (поверхня)
player_img = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.draw.circle(player_img, CRACK_BLUE, (20, 20), 20) 
pygame.draw.circle(player_img, (100, 150, 255), (20, 20), 15) 

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