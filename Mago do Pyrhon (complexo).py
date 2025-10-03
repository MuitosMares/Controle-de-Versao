```python
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_SIZE = 32
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
HEALTH_BAR_WIDTH = 300
HEALTH_BAR_HEIGHT = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
LIGHT_BLUE = (135, 206, 235)
GRAY = (128, 128, 128)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Magic Combat Game")
font = pygame.font.SysFont(None, FONT_SIZE)
large_font = pygame.font.SysFont(None, 48)

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# Effect class for animations
class Effect:
    def __init__(self, x, y, text, color, duration=60):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.duration = duration
        self.alpha = 255
        self.dy = -2  # Move upwards

    def update(self):
        self.y += self.dy
        self.alpha -= 4
        if self.alpha < 0:
            self.alpha = 0
        self.duration -= 1

    def draw(self, screen):
        if self.duration > 0:
            text_surf = font.render(self.text, True, self.color)
            text_surf.set_alpha(self.alpha)
            screen.blit(text_surf, (self.x, self.y))

# Game class
class Game:
    def __init__(self):
        self.player_health = 100
        self.max_player_health = 100
        self.enemy_health = 100
        self.potion_uses = 2
        self.effects = []
        self.game_over = False
        self.winner = None
        self.player_turn = True
        self.message = ""
        self.message_timer = 0

        # Buttons
        button_y = SCREEN_HEIGHT - 200
        self.buttons = [
            Button(50, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Fireball (30 dmg, 60%)", ORANGE, (255, 200, 0)),
            Button(300, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Ice Bolt (20 dmg, 80%)", LIGHT_BLUE, (173, 216, 230)),
            Button(550, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Meteor (50 dmg, 30%)", PURPLE, (186, 85, 211)),
            Button(50, button_y + 70, BUTTON_WIDTH, BUTTON_HEIGHT, "Potion (Heal 35)", GREEN, (144, 238, 144)),
            Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50, "Restart", GRAY, (169, 169, 169))
        ]
        self.restart_button = self.buttons[-1]
        self.restart_button.rect.y = SCREEN_HEIGHT // 2 + 100  # Position for game over

    def add_effect(self, x, y, text, color):
        self.effects.append(Effect(x, y, text, color))

    def player_attack(self, spell):
        damage = 0
        hit_chance = 0
        effect_color = WHITE
        message = ""
        if spell == 0:  # Fireball
            damage = 30
            hit_chance = 60
            effect_color = RED
            message = "Fireball!"
        elif spell == 1:  # Ice Bolt
            damage = 20
            hit_chance = 80
            effect_color = BLUE
            message = "Ice Bolt!"
        elif spell == 2:  # Meteor
            damage = 50
            hit_chance = 30
            effect_color = PURPLE
            message = "Meteor!"
        elif spell == 3:  # Potion
            if self.potion_uses > 0:
                self.potion_uses -= 1
                heal_amount = 35 if self.player_health <= 65 else self.max_player_health - self.player_health
                self.player_health += heal_amount
                if self.player_health > self.max_player_health:
                    self.player_health = self.max_player_health
                self.add_effect(100, 100, f"+{heal_amount} HP", GREEN)
                self.message = f"Potion used! {self.potion_uses} left."
            else:
                self.message = "No potions left!"
            self.message_timer = 60
            self.player_turn = False
            return

        self.add_effect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, message, effect_color)
        if random.randint(1, 100) <= hit_chance:
            self.enemy_health -= damage
            self.add_effect(600, 100, f"-{damage}", RED)
            self.message = "Hit!"
        else:
            self.add_effect(600, 100, "Miss!", WHITE)
            self.message = "Missed!"
        self.message_timer = 60

        if self.enemy_health <= 0:
            self.game_over = True
            self.winner = "Player"
        else:
            self.player_turn = False

    def enemy_attack(self):
        spells = [
            (30, 60, RED, "Enemy Fireball!"),
            (20, 80, BLUE, "Enemy Ice Bolt!"),
            (50, 30, PURPLE, "Enemy Meteor!")
        ]
        damage, hit_chance, color, message = random.choice(spells)
        self.add_effect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, message, color)
        if random.randint(1, 100) <= hit_chance:
            self.player_health -= damage
            self.add_effect(100, 100, f"-{damage}", RED)
            self.message = "Enemy Hit!"
        else:
            self.add_effect(100, 100, "Enemy Miss!", WHITE)
            self.message = "Enemy Missed!"
        self.message_timer = 60

        if self.player_health <= 0:
            self.game_over = True
            self.winner = "Enemy"
        self.player_turn = True

    def update(self):
        if self.message_timer > 0:
            self.message_timer -= 1
        for effect in self.effects[:]:
            effect.update()
            if effect.duration <= 0:
                self.effects.remove(effect)

        if not self.player_turn and not self.game_over and self.message_timer == 0:
            self.enemy_attack()

    def draw(self, screen):
        screen.fill(BLACK)

        # Player health
        pygame.draw.rect(screen, GRAY, (50, 50, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
        player_health_width = (self.player_health / self.max_player_health) * HEALTH_BAR_WIDTH
        pygame.draw.rect(screen, GREEN, (50, 50, player_health_width, HEALTH_BAR_HEIGHT))
        player_text = font.render(f"Player: {self.player_health}/{self.max_player_health}", True, WHITE)
        screen.blit(player_text, (50, 20))

        # Enemy health
        pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH - HEALTH_BAR_WIDTH - 50, 50, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT))
        enemy_health_width = (self.enemy_health / 100) * HEALTH_BAR_WIDTH
        pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH - HEALTH_BAR_WIDTH - 50, 50, enemy_health_width, HEALTH_BAR_HEIGHT))
        enemy_text = font.render(f"Enemy: {self.enemy_health}/100", True, WHITE)
        screen.blit(enemy_text, (SCREEN_WIDTH - HEALTH_BAR_WIDTH - 50, 20))

        # Potions
        potion_text = font.render(f"Potions: {self.potion_uses}", True, WHITE)
        screen.blit(potion_text, (50, 80))

        # Message
        if self.message_timer > 0:
            msg_text = font.render(self.message, True, WHITE)
            screen.blit(msg_text, (SCREEN_WIDTH // 2 - msg_text.get_width() // 2, SCREEN_HEIGHT - 250))

        # Buttons
        if not self.game_over:
            for i in range(4):
                self.buttons[i].draw(screen)
        else:
            result_text = large_font.render("You Win!" if self.winner == "Player" else "You Lose!", True, GREEN if self.winner == "Player" else RED)
            screen.blit(result_text, (SCREEN_WIDTH // 2 - result_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            self.restart_button.draw(screen)

        # Effects
        for effect in self.effects:
            effect.draw(screen)

    def handle_event(self, event):
        if self.game_over:
            if self.restart_button.is_clicked(event):
                self.__init__()
            return

        if not self.player_turn:
            return

        for i in range(4):
            if self.buttons[i].is_clicked(event):
                self.player_attack(i)
                break

    def check_hover(self, pos):
        if not self.game_over:
            for i in range(4):
                self.buttons[i].check_hover(pos)
        else:
            self.restart_button.check_hover(pos)

# Main loop
game = Game()
clock = pygame.time.Clock()

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    game.check_hover(mouse_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        game.handle_event(event)

    game.update()
    game.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
```