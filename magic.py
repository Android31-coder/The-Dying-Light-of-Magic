import pygame
import sys
import os
import math
import random

# Ініціалізація
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Dying Light of Magic")

# Кольори
BLACK = (10, 10, 15)
BONE_WHITE = (235, 225, 210)
RUIN_GOLD = (180, 150, 50)
CRACK_BLUE = (70, 130, 180)
MAP_BG = (20, 20, 30, 200)

# Розмір тайлів і світу
TILE_SIZE = 64
WORLD_WIDTH = 100  # у тайлах
WORLD_HEIGHT = 100 # у тайлах

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
world_tiles = []
for y in range(WORLD_HEIGHT):
    row = []
    for x in range(WORLD_WIDTH):
        # Генерація різних біомів
        noise = random.random()
        
        if y < 20:  # Північ - сніги
            if noise > 0.9:
                row.append('stone')
            else:
                row.append('snow')
        elif y < 40:  # Гори
            if x < 20 or x > 80:
                row.append('stone')
            else:
                if noise > 0.7:
                    row.append('stone')
                else:
                    row.append('snow')
        elif y < 60:  # Ліси
            if noise > 0.85:
                row.append('dark_grass')
            else:
                row.append('grass')
        elif y < 80:  # Рівнини
            if noise > 0.7:
                row.append('sand')
            else:
                row.append('grass')
        else:  # Південь - пустеля
            if noise > 0.95:
                row.append('stone')
            else:
                row.append('sand')
                
        # Додаємо річки
        if (x + y) % 30 == 0 or (x - y) % 45 == 0:
            for i in range(1, 4):
                if y+i < WORLD_HEIGHT:
                    if len(world_tiles) > y+i-1 and len(row) > x:
                        world_tiles[y+i-1][x] = 'water'
    world_tiles.append(row)

# Гравець
player_img = pygame.Surface((40, 40), pygame.SRCALPHA)
pygame.draw.circle(player_img, CRACK_BLUE, (20, 20), 20)
pygame.draw.circle(player_img, (100, 150, 255), (20, 20), 15)

# Шрифти
try:
    title_font = pygame.font.Font("fonts/CinzelDecorative-Bold.ttf", 80)
    menu_font = pygame.font.Font(None, 50)
    map_font = pygame.font.Font(None, 24)
except:
    title_font = pygame.font.Font(None, 80)
    menu_font = pygame.font.Font(None, 50)
    map_font = pygame.font.Font(None, 24)

# Завантаження ресурсів
try:
    background = pygame.transform.scale(pygame.image.load("fon.jpg"), (WIDTH, HEIGHT))
except:
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(BLACK)

# Мапа
try:
    world_map = pygame.image.load("map.jpg").convert()
except:
    world_map = pygame.Surface((2000, 2000))
    world_map.fill((30, 30, 40))

# Налаштування музики
try:
    pygame.mixer.music.load("bog_creatures_on_the_move.mp3")
    pygame.mixer.music.set_volume(0.5)
    music_playing = True
    pygame.mixer.music.play(-1)
except:
    music_playing = False

class Button:
    def __init__(self, text, x, y, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.action = action
        self.is_hovered = False
    
    def draw(self):
        color = RUIN_GOLD if self.is_hovered else BONE_WHITE
        text = menu_font.render(self.text, True, color)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)
        return text_rect
    
    def check_hover(self, pos):
        text_rect = self.draw()
        self.is_hovered = text_rect.collidepoint(pos)

def fade_transition():
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill(BLACK)
    for alpha in range(0, 255, 5):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)

def show_story():
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
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False
        
        screen.fill(BLACK)
        for i, surf in enumerate(text_surfaces):
            surf.set_alpha(alpha)
            rect = surf.get_rect(center=(WIDTH//2, 100 + i * 50))
            screen.blit(surf, rect)
        
        if alpha < 255:
            alpha += 3

        pygame.display.flip()
        clock.tick(60)

def draw_minimap(player_pos, visible_area):
    # Розміри мінімапи
    minimap_width, minimap_height = 200, 150
    minimap_x, minimap_y = WIDTH - minimap_width - 20, HEIGHT - minimap_height - 20

    # Створення поверхні для мінімапи
    minimap_surface = pygame.Surface((minimap_width, minimap_height), pygame.SRCALPHA)
    minimap_surface.fill((*BLACK, 150))

    # Зменшена копія великої мапи
    try:
        map_scaled = pygame.transform.smoothscale(world_map, (minimap_width, minimap_height))
        minimap_surface.blit(map_scaled, (0, 0))
    except:
        pygame.draw.rect(minimap_surface, CRACK_BLUE, (0, 0, minimap_width, minimap_height), 1)

    # Визначення прямокутника видимої області
    map_scale_x = minimap_width / world_map.get_width()
    map_scale_y = minimap_height / world_map.get_height()

    player_map_x = int(player_pos[0] * map_scale_x)
    player_map_y = int(player_pos[1] * map_scale_y)

    # Гравець на мінімапі
    pygame.draw.circle(minimap_surface, BONE_WHITE, (player_map_x, player_map_y), 4)

    # Вивід на екран
    screen.blit(minimap_surface, (minimap_x, minimap_y))

def draw_world_map(player_pos, show_full_map):
    if not show_full_map:
        return

    # Розтягуємо карту на весь екран
    map_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    map_surface.fill((*BLACK, 200))

    # Повний розмір мапи (без масштабу 0.4)
    scaled_map = pygame.transform.scale(world_map, (WIDTH, HEIGHT))
    map_surface.blit(scaled_map, (0, 0))

    # Позиція гравця
    map_scale_x = WIDTH / world_map.get_width()
    map_scale_y = HEIGHT / world_map.get_height()
    player_map_x = int(player_pos[0] * map_scale_x)
    player_map_y = int(player_pos[1] * map_scale_y)

    # Позначка гравця
    pygame.draw.circle(map_surface, BONE_WHITE, (player_map_x, player_map_y), 4)

    # Назва
    title = title_font.render("Карта світу", True, RUIN_GOLD)
    map_surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

    screen.blit(map_surface, (0, 0))

def draw_world(player_pos):
    # Визначаємо, які тайли потрібно відобразити
    start_x = max(0, int(player_pos[0] / TILE_SIZE - WIDTH // (2 * TILE_SIZE)))
    start_y = max(0, int(player_pos[1] / TILE_SIZE - HEIGHT // (2 * TILE_SIZE)))
    end_x = min(WORLD_WIDTH, start_x + WIDTH // TILE_SIZE + 2)
    end_y = min(WORLD_HEIGHT, start_y + HEIGHT // TILE_SIZE + 2)
    
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            # Позиція тайла на екрані
            screen_x = x * TILE_SIZE - player_pos[0] + WIDTH // 2
            screen_y = y * TILE_SIZE - player_pos[1] + HEIGHT // 2
            
            # Малюємо тайл
            tile_type = world_tiles[y][x]
            screen.blit(textures[tile_type], (screen_x, screen_y))
            
            # Додаткові деталі
            if tile_type == 'grass' and random.random() > 0.9:
                pygame.draw.circle(screen, (0, random.randint(100, 150), 0), 
                                 (screen_x + random.randint(5, TILE_SIZE-5), 
                                  screen_y + random.randint(5, TILE_SIZE-5)), 
                                 random.randint(1, 3))

class Player:
    def __init__(self, name="Відлюдник", position=(640, 360)):
        self.name = name
        self.position = list(position)
        self.health = 100
        self.mana = 50
        self.speed = 5
        self.strength = 10
        self.inventory = []
        self.quests = []

    def move(self, dx, dy):
        self.position[0] += dx * self.speed
        self.position[1] += dy * self.speed

class Quest:
    def __init__(self, title, description, objective, reward):
        self.title = title
        self.description = description
        self.objective = objective
        self.reward = reward
        self.completed = False

    def check_completion(self, player):
        if self.objective in player.inventory and not self.completed:
            self.completed = True
            player.inventory.append(self.reward)
            return True
        return False

class NPC:
    def __init__(self, name, position, dialogue, quest=None):
        self.name = name
        self.position = position
        self.dialogue = dialogue
        self.quest = quest
        self.quest_given = False

    def interact(self, player):
        if self.quest and not self.quest_given:
            player.quests.append(self.quest)
            self.quest_given = True
            return f"{self.name}: {self.dialogue} (Квест додано)"
        elif self.quest and self.quest.check_completion(player):
            return f"{self.name}: Молодець! {self.quest.title} завершено."
        else:
            return f"{self.name}: {self.dialogue}"

def game_loop():
    clock = pygame.time.Clock()
    player_pos = [WORLD_WIDTH * TILE_SIZE // 2, WORLD_HEIGHT * TILE_SIZE // 2]
    player_speed = 5
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
                elif event.key == pygame.K_m:  # Перемикач мапи
                    show_full_map = not show_full_map
        
        # Керування гравцем
        keys = pygame.key.get_pressed()
        move_x, move_y = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x += player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move_y -= player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_y += player_speed
        
        # Оновлення позиції гравця
        player_pos[0] = max(0, min(WORLD_WIDTH * TILE_SIZE - 1, player_pos[0] + move_x))
        player_pos[1] = max(0, min(WORLD_HEIGHT * TILE_SIZE - 1, player_pos[1] + move_y))
        
        # Відображення
        draw_world(player_pos)
        
        # Малюємо гравця (завжди в центрі екрана)
        screen.blit(player_img, (WIDTH//2 - 20, HEIGHT//2 - 20))
        
        # Мінімапа
        draw_minimap(player_pos, (WIDTH*2, HEIGHT*2))
        
        # Повна мапа (якщо відкрита)
        draw_world_map(player_pos, show_full_map)
        
        pygame.display.flip()
        clock.tick(60)

def main_menu():
    clock = pygame.time.Clock()
    
    buttons = [
        Button("Нова гра", WIDTH // 2, HEIGHT // 2 - 60, action=start_new_game),
        Button("Налаштування", WIDTH // 2, HEIGHT // 2 + 20, action=settings_menu),
        Button("Вийти", WIDTH // 2, HEIGHT // 2 + 100, action=lambda: pygame.quit() or sys.exit())
    ]
    
    music_btn = Button("Музика: ON", WIDTH - 130, HEIGHT - 30)
    
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
                
                if music_btn.is_hovered:
                    global music_playing
                    music_playing = not music_playing
                    if music_playing:
                        pygame.mixer.music.unpause()
                        music_btn.text = "Музика: ON"
                    else:
                        pygame.mixer.music.pause()
                        music_btn.text = "Музика: OFF"
        
        for btn in buttons:
            btn.check_hover(mouse_pos)
        music_btn.check_hover(mouse_pos)
        
        screen.blit(background, (0, 0))
        
        # ==== ЕФЕКТ ПУЛЬСАЦІЇ ====
        tick = pygame.time.get_ticks() / 1000  # час у секундах
        pulse = (math.sin(tick * 2) + 1) / 2  # значення від 0 до 1
        
        # Плавне змішування RUIN_GOLD і BONE_WHITE
        r = int(RUIN_GOLD[0] * pulse + BONE_WHITE[0] * (1 - pulse))
        g = int(RUIN_GOLD[1] * pulse + BONE_WHITE[1] * (1 - pulse))
        b = int(RUIN_GOLD[2] * pulse + BONE_WHITE[2] * (1 - pulse))
        title_color = (r, g, b)
        
        title = title_font.render("The Dying Light of Magic", True, title_color)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 6))  # трохи піднято
        
        for btn in buttons:
            btn.draw()
        music_btn.draw()
        
        pygame.display.flip()
        clock.tick(60) 

def start_new_game():
    show_story()
    game_loop()

def settings_menu():
    clock = pygame.time.Clock()
    back_btn = Button("Назад", WIDTH // 2, HEIGHT // 2 + 180)

    # Повзунок гучності
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

        screen.blit(background, (0, 0))
        title = title_font.render("Налаштування", True, BONE_WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

        # Повзунок фон
        pygame.draw.rect(screen, (*BLACK, 150), (slider_x, slider_y, slider_width, slider_height), 0, 10)
        pygame.draw.rect(screen, (*CRACK_BLUE, 100), (slider_x, slider_y, slider_width, slider_height), 1, 10)

        # Активна частина
        active_width = slider_pos - slider_x
        if active_width > 0:
            active_slider = pygame.Surface((active_width, slider_height), pygame.SRCALPHA)
            pygame.draw.rect(active_slider, (*RUIN_GOLD, 200), (0, 0, active_width, slider_height), 0, 10)
            screen.blit(active_slider, (slider_x, slider_y))

        # Кружечок
        pygame.draw.circle(screen, BONE_WHITE, (slider_pos, slider_y + slider_height // 2), 12)
        pygame.draw.circle(screen, RUIN_GOLD, (slider_pos, slider_y + slider_height // 2), 10)
        pygame.draw.circle(screen, CRACK_BLUE, (slider_pos, slider_y + slider_height // 2), 8)

        # Текст
        volume_text = menu_font.render("Гучність", True, BONE_WHITE)
        screen.blit(volume_text, (slider_x - volume_text.get_width() - 40, slider_y - 5))

        back_btn.draw()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()