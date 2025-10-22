# ui.py - Функції для відображення мапи, анімації переходу, історії

import pygame
import math
from assets import screen, title_font, menu_font, world_map, background
from config import WIDTH, HEIGHT, BLACK, BONE_WHITE, RUIN_GOLD, CRACK_BLUE

def fade_transition():
    # Ефект затемнення
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill(BLACK)
    for alpha in range(0, 255, 5):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)

def show_story():
    # Логіка історії
    clock = pygame.time.Clock()
    story_text = [
        "Передісторія світу:",
        "Колись цей світ був звичайним — королівства, торгівля, війни.",
        "Рік 0: вторгнення істот крізь портали, звичайна зброя безсила.",
        "Рік 1-5: пробудження магії серед людей, зміна балансу.",
        "Рік 7: Велика Криза Мани, вибух Серця під столицею.",
        "Сьогодення: уламки магії змінюють світ, мутації, фантоми.",
        "Відлюдник — єдиний, хто може вбирати уламки без мутацій.",
        "Його мета: знайти 7 Слідів Серця й вирішити долю світу...",
        "Натисни будь-яку клавішу, щоб продовжити."
    ]

    waiting = True
    alpha = 0
    text_surfaces = [menu_font.render(line, True, BONE_WHITE) for line in story_text]

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit() 
            elif event.type == pygame.KEYDOWN:
                waiting = False
                return 
        
        screen.fill(BLACK)
        for i, surf in enumerate(text_surfaces):
            surf.set_alpha(alpha)
            rect = surf.get_rect(center=(WIDTH//2, 100 + i * 50))
            screen.blit(surf, rect)
        
        if alpha < 255:
            alpha += 3

        pygame.display.flip()
        clock.tick(60)

def draw_minimap(player_pos):
    # Відображення мінімапи в куті
    minimap_width, minimap_height = 200, 150
    minimap_x, minimap_y = WIDTH - minimap_width - 20, HEIGHT - minimap_height - 20

    minimap_surface = pygame.Surface((minimap_width, minimap_height), pygame.SRCALPHA)
    minimap_surface.fill((*BLACK, 150))

    try:
        map_scaled = pygame.transform.smoothscale(world_map, (minimap_width, minimap_height))
        minimap_surface.blit(map_scaled, (0, 0))
    except:
        pygame.draw.rect(minimap_surface, CRACK_BLUE, (0, 0, minimap_width, minimap_height), 1)

    map_scale_x = minimap_width / world_map.get_width()
    map_scale_y = minimap_height / world_map.get_height()

    player_map_x = int(player_pos[0] * map_scale_x)
    player_map_y = int(player_pos[1] * map_scale_y)

    pygame.draw.circle(minimap_surface, BONE_WHITE, (player_map_x, player_map_y), 4)
    screen.blit(minimap_surface, (minimap_x, minimap_y))

def draw_world_map(player_pos, show_full_map):
    # Відображення повної карти світу
    if not show_full_map:
        return

    map_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    map_surface.fill((*BLACK, 200))

    scaled_map = pygame.transform.scale(world_map, (WIDTH, HEIGHT))
    map_surface.blit(scaled_map, (0, 0))

    map_scale_x = WIDTH / world_map.get_width()
    map_scale_y = HEIGHT / world_map.get_height()
    player_map_x = int(player_pos[0] * map_scale_x)
    player_map_y = int(player_pos[1] * map_scale_y)

    pygame.draw.circle(map_surface, BONE_WHITE, (player_map_x, player_map_y), 4)

    title = title_font.render("Карта світу", True, RUIN_GOLD)
    map_surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

    screen.blit(map_surface, (0, 0))

def draw_settings_ui(slider_pos, slider_x, slider_y, slider_width, slider_height, back_btn):
    # Відображення UI налаштувань
    screen.blit(background, (0, 0))
    title = title_font.render("Налаштування", True, BONE_WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

    # Повзунок фон
    pygame.draw.rect(screen, BLACK, (slider_x, slider_y, slider_width, slider_height), 0, 10)
    pygame.draw.rect(screen, CRACK_BLUE, (slider_x, slider_y, slider_width, slider_height), 1, 10)

    # Активна частина
    active_width = slider_pos - slider_x
    if active_width > 0:
        active_slider = pygame.Surface((active_width, slider_height), pygame.SRCALPHA)
        pygame.draw.rect(active_slider, RUIN_GOLD, (0, 0, active_width, slider_height), 0, 10)
        screen.blit(active_slider, (slider_x, slider_y))

    # Кружечок
    pygame.draw.circle(screen, BONE_WHITE, (slider_pos, slider_y + slider_height // 2), 12)
    pygame.draw.circle(screen, RUIN_GOLD, (slider_pos, slider_y + slider_height // 2), 10)
    pygame.draw.circle(screen, CRACK_BLUE, (slider_pos, slider_y + slider_height // 2), 8)

    # Текст
    volume_text = menu_font.render("Гучність", True, BONE_WHITE)
    screen.blit(volume_text, (slider_x - volume_text.get_width() - 40, slider_y - 5))

    back_btn.draw()