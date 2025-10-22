# entities.py - Класи для гравця, кнопок, квестів та NPC

from assets import menu_font, screen
from config import RUIN_GOLD, BONE_WHITE, CRACK_BLUE, PLAYER_SPEED

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

class Player:
    def __init__(self, name="Відлюдник", position=(640, 360)):
        self.name = name
        self.position = list(position)
        self.health = 100
        self.mana = 50
        self.speed = PLAYER_SPEED # Використовуємо константу
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