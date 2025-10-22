# world.py - Логіка генерації світу та малювання тайлів

import pygame
import random
from config import TILE_SIZE, WORLD_WIDTH, WORLD_HEIGHT
from assets import screen

# Функція для створення текстур тайлів
def create_tile_surface(color, variation=False):
    tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
    tile.fill(color)
    if variation:
        variation = random.randint(-10, 10)
        r = max(0, min(255, color[0] + variation))
        g = max(0, min(255, color[1] + variation))
        b = max(0, min(255, color[2] + variation))
        pygame.draw.rect(tile, (r, g, b), 
                         (random.randint(0, TILE_SIZE//2), 
                          random.randint(0, TILE_SIZE//2), 
                          random.randint(TILE_SIZE//4, TILE_SIZE//2), 
                          random.randint(TILE_SIZE//4, TILE_SIZE//2)))
    return tile

# Створення текстур для різних типів місцевості
textures = {
    'grass': create_tile_surface((34, 139, 34), True),
    'sand': create_tile_surface((194, 178, 128), True),
    'stone': create_tile_surface((105, 105, 105)),
    'water': create_tile_surface((65, 105, 225)),
    'snow': create_tile_surface((220, 220, 255), True),
    'dirt': create_tile_surface((139, 69, 19), True),
    'dark_grass': create_tile_surface((0, 100, 0), True)
}

# Генерація світу
def generate_world():
    world_tiles_data = []
    for y in range(WORLD_HEIGHT):
        row = []
        for x in range(WORLD_WIDTH):
            noise = random.random()
            
            # Логіка генерації біомів
            if y < 20: 
                row.append('stone' if noise > 0.9 else 'snow')
            elif y < 40: 
                if x < 20 or x > 80 or noise > 0.7:
                    row.append('stone')
                else:
                    row.append('snow')
            elif y < 60:
                row.append('dark_grass' if noise > 0.85 else 'grass')
            elif y < 80:
                row.append('sand' if noise > 0.7 else 'grass')
            else:
                row.append('stone' if noise > 0.95 else 'sand')
                
        world_tiles_data.append(row)

    # Додаємо річки
    for y in range(WORLD_HEIGHT):
        for x in range(WORLD_WIDTH):
             if (x + y) % 30 == 0 or (x - y) % 45 == 0:
                for i in range(1, 4):
                    if y + i < WORLD_HEIGHT and x < WORLD_WIDTH:
                        if y + i - 1 < len(world_tiles_data) and x < len(world_tiles_data[y+i-1]):
                            world_tiles_data[y + i - 1][x] = 'water'
                        
    return world_tiles_data

# Глобальна змінна світу, згенерована один раз при запуску
WORLD_TILES = generate_world()


def draw_world(player_pos):
    # Визначаємо область для відображення
    width, height = screen.get_size()
    start_x = max(0, int(player_pos[0] / TILE_SIZE - (width // (2 * TILE_SIZE))))
    start_y = max(0, int(player_pos[1] / TILE_SIZE - (height // (2 * TILE_SIZE))))
    end_x = min(WORLD_WIDTH, start_x + width // TILE_SIZE + 2)
    end_y = min(WORLD_HEIGHT, start_y + height // TILE_SIZE + 2)
    
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            screen_x = x * TILE_SIZE - player_pos[0] + width // 2
            screen_y = y * TILE_SIZE - player_pos[1] + height // 2
            
            tile_type = WORLD_TILES[y][x]
            screen.blit(textures[tile_type], (screen_x, screen_y))
            
            # Додаткові деталі (трава)
            if tile_type == 'grass' and random.random() > 0.9:
                pygame.draw.circle(screen, (0, random.randint(100, 150), 0), 
                                 (screen_x + random.randint(5, TILE_SIZE-5), 
                                  screen_y + random.randint(5, TILE_SIZE-5)), 
                                 random.randint(1, 3))