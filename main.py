# main.py - Точка входу, головний цикл, меню та логіка гри

import pygame
import sys
import math
from ui import show_story, fade_transition, draw_minimap, draw_world_map, draw_settings_ui
from config import WIDTH, HEIGHT, TILE_SIZE, WORLD_WIDTH, WORLD_HEIGHT, RUIN_GOLD, BONE_WHITE, PLAYER_SPEED
from assets import screen, background, title_font, get_music_state, toggle_music, Player
from entities import Button
from world import draw_world

player = Player((WIDTH // 2, HEIGHT // 2))

def game_loop():
    clock = pygame.time.Clock()
    # Початкова позиція гравця в центрі світу
    player_pos = [WORLD_WIDTH * TILE_SIZE // 2, WORLD_HEIGHT * TILE_SIZE // 2]
    show_full_map = False
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    fade_transition()
                    return
                elif event.key == pygame.K_m: 
                    show_full_map = not show_full_map
        
        # Керування гравцем
        keys = pygame.key.get_pressed()
        move_x, move_y = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x += PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move_y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_y += PLAYER_SPEED
        
        # Обмеження позиції
        world_max_x = WORLD_WIDTH * TILE_SIZE - 1
        world_max_y = WORLD_HEIGHT * TILE_SIZE - 1
        player_pos[0] = max(0, min(world_max_x, player_pos[0] + move_x))
        player_pos[1] = max(0, min(world_max_y, player_pos[1] + move_y))
        
        # Відображення світу
        draw_world(player_pos)
    
        # Малюємо гравця (завжди в центрі екрана)
        player.update()
        screen.blit(player.image, (WIDTH//2 - 20, HEIGHT//2 - 20))
        # UI
        draw_minimap(player_pos)
        draw_world_map(player_pos, show_full_map)
        
        pygame.display.flip()
        clock.tick(60)

def start_new_game():
    show_story()
    game_loop()

def settings_menu():
    clock = pygame.time.Clock()
    back_btn = Button("Назад", WIDTH // 2, HEIGHT // 2 + 180)

    # Повзунок гучності: Конфігурація
    slider_width = 350
    slider_height = 12
    slider_x = WIDTH // 2 - slider_width // 2
    slider_y = HEIGHT // 2 + 20
    slider_pos = slider_x + int(pygame.mixer.music.get_volume() * slider_width)
    slider_active = False

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.is_hovered:
                    return 
                slider_rect = pygame.Rect(slider_x, slider_y - 15, slider_width, 30)
                if slider_rect.collidepoint(mouse_pos):
                    slider_active = True

            if event.type == pygame.MOUSEBUTTONUP:
                slider_active = False

            if event.type == pygame.MOUSEMOTION and slider_active:
                slider_pos = max(slider_x, min(mouse_pos[0], slider_x + slider_width))
                volume = (slider_pos - slider_x) / slider_width
                pygame.mixer.music.set_volume(volume)

        back_btn.check_hover(mouse_pos)

        # Рендеринг UI налаштувань (винесено у ui.py)
        draw_settings_ui(slider_pos, slider_x, slider_y, slider_width, slider_height, back_btn)
        
        pygame.display.flip()
        clock.tick(60)

def main_menu():
    clock = pygame.time.Clock()
    
    buttons = [
        Button("Нова гра", WIDTH // 2, HEIGHT // 2 - 60, action=start_new_game),
        Button("Налаштування", WIDTH // 2, HEIGHT // 2 + 20, action=settings_menu),
        Button("Вийти", WIDTH // 2, HEIGHT // 2 + 100, action=lambda: pygame.quit() or sys.exit())
    ]
    
    initial_text = "Музика: ON" if get_music_state() else "Музика: OFF"
    music_btn = Button(initial_text, WIDTH - 130, HEIGHT - 30)
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn.is_hovered and btn.action:
                        fade_transition()
                        btn.action()
                
                # Обробка кнопки музики
                if music_btn.is_hovered:
                    new_state = toggle_music()
                    music_btn.text = "Музика: ON" if new_state else "Музика: OFF"
        
        for btn in buttons:
            btn.check_hover(mouse_pos)
        music_btn.check_hover(mouse_pos)
        
        screen.blit(background, (0, 0))
        
        # ЕФЕКТ ПУЛЬСАЦІЇ
        tick = pygame.time.get_ticks() / 1000 
        pulse = (math.sin(tick * 2) + 1) / 2 
        
        r = int(RUIN_GOLD[0] * pulse + BONE_WHITE[0] * (1 - pulse))
        g = int(RUIN_GOLD[1] * pulse + BONE_WHITE[1] * (1 - pulse))
        b = int(RUIN_GOLD[2] * pulse + BONE_WHITE[2] * (1 - pulse))
        title_color = (r, g, b)
        
        title = title_font.render("The Dying Light of Magic", True, title_color)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 6))
        
        for btn in buttons:
            btn.draw()
        music_btn.draw()
        
        pygame.display.flip()
        clock.tick(60) 
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()