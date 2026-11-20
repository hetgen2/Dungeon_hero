
import math

import pygame

from config import (
    WIDTH, HEIGHT, TOTAL_WAVES, ATTACK_DISTANCE, ATTACK_HALF_ANGLE_DEG,
)
from model.boss import Boss, BossState
from model.combat import aim_angle
from view import colors

FONT_SIZE = 48
BIG_FONT_SIZE = 96
HEART_SIZE = 40
HEART_STEP = 50
HUD_MARGIN = 20
HUD_RIGHT_X = WIDTH - 180
BLINK_RATE = 12            
FAN_STEP_DEG = 2
FAN_LINE_WIDTH = 8
BOSS_BAR_WIDTH = 400
BOSS_BAR_HEIGHT = 25
BOSS_BAR_Y = 60
OUTLINE = 3


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.big_font = pygame.font.Font(None, BIG_FONT_SIZE)

    #Игровой экран
    def draw_world(self, world, mouse_pos):
        self.screen.fill(colors.BLACK)
        self._draw_hud(world)
        if world.player.is_attacking:
            self._draw_attack_fan(world.player, mouse_pos)
        for enemy in world.enemies:
            if isinstance(enemy, Boss):
                self._draw_boss(enemy)
            else:
                self._draw_enemy(enemy)
        self._draw_player(world.player)

    def _draw_hud(self, world):
        for i in range(world.player.hp):
            heart = (HUD_MARGIN + i * HEART_STEP, HUD_MARGIN, HEART_SIZE, HEART_SIZE)
            pygame.draw.rect(self.screen, colors.RED, heart)
            pygame.draw.rect(self.screen, colors.WHITE, heart, OUTLINE)

        self._draw_text(f"ВОЛНА:{world.wave}/{TOTAL_WAVES}", (HUD_RIGHT_X, HUD_MARGIN))
        self._draw_text(f"ВРАГОВ:{len(world.enemies)}", (HUD_RIGHT_X, 70))

        if not world.wave_in_progress:
            text = self.big_font.render("СЛЕДУЮЩАЯ ВОЛНА", True, colors.YELLOW)
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))

    def _draw_player(self, player):
        blinking = player.is_invincible and int(player.invincible_timer * BLINK_RATE) % 2 == 0
        color = colors.GRAY if blinking else colors.BLUE
        rect = pygame.Rect(int(player.x), int(player.y), player.width, player.height)
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, colors.WHITE, rect, OUTLINE)

    def _draw_attack_fan(self, player, mouse_pos):
        center = player.center
        base_angle = aim_angle(center, mouse_pos)
        for offset in range(-ATTACK_HALF_ANGLE_DEG, ATTACK_HALF_ANGLE_DEG + 1, FAN_STEP_DEG):
            angle = base_angle + math.radians(offset)
            end = (center[0] + math.cos(angle) * ATTACK_DISTANCE,
                   center[1] + math.sin(angle) * ATTACK_DISTANCE)
            pygame.draw.line(self.screen, colors.WHITE, center, end, FAN_LINE_WIDTH)

    #Враги
    def _draw_enemy(self, enemy):
        cx, cy = int(enemy.center[0]), int(enemy.center[1])
        radius = enemy.width // 2
        pygame.draw.circle(self.screen, colors.ENEMY_COLORS[enemy.kind], (cx, cy), radius)
        pygame.draw.circle(self.screen, colors.BLACK, (cx, cy), radius, 2)
        self._draw_eyes(cx, cy, radius)
        if enemy.show_hp:
            self._draw_text(str(enemy.hp), (int(enemy.x) + 15, int(enemy.y) - 20))

    def _draw_eyes(self, cx, cy, radius):
        eye_radius = radius // 3
        offset_x = radius // 2
        offset_y = radius // 3
        for side in (-1, 1):
            eye = (cx + side * offset_x, cy - offset_y)
            pygame.draw.circle(self.screen, colors.WHITE, eye, eye_radius)
            pygame.draw.circle(self.screen, colors.BLACK, eye, eye_radius // 2)

    def _draw_boss(self, boss):
        charging = boss.state is BossState.CHARGING
        color = colors.BOSS_CHARGING if charging else colors.ENEMY_COLORS["boss"]
        rect = pygame.Rect(int(boss.x), int(boss.y), boss.width, boss.height)
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, colors.YELLOW, rect, 4)
        self._draw_boss_bar(boss)

    def _draw_boss_bar(self, boss):
        bar_x = WIDTH // 2 - BOSS_BAR_WIDTH // 2
        filled = BOSS_BAR_WIDTH * boss.hp / boss.max_hp
        pygame.draw.rect(self.screen, colors.RED, (bar_x, BOSS_BAR_Y, filled, BOSS_BAR_HEIGHT))
        text = self.font.render(f"BOSS: {boss.hp}/{boss.max_hp}", True, colors.WHITE)
        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, BOSS_BAR_Y - 30))

    #друггие экраны
    def draw_menu(self, buttons, mouse_pos):
        self.screen.fill(colors.BLACK)
        self._draw_centered("DUNGEON HERO", self.big_font, colors.WHITE, 150)
        self._draw_centered("WASD - движение, ЛКМ - атака", self.font, colors.GRAY, 280)
        self._draw_buttons(buttons, mouse_pos)

    def draw_end_screen(self, title, title_color, subtitle, buttons, mouse_pos):
        self.screen.fill(colors.BLACK)
        self._draw_centered(title, self.big_font, title_color, 350)
        if subtitle:
            self._draw_centered(subtitle, self.font, colors.WHITE, 450)
        self._draw_buttons(buttons, mouse_pos)

    #Вспомогательные
    def _draw_buttons(self, buttons, mouse_pos):
        for button in buttons:
            hovered = button.contains(mouse_pos)
            pygame.draw.rect(self.screen, button.hover_color if hovered else button.color, button.rect)
            pygame.draw.rect(self.screen, colors.WHITE, button.rect, OUTLINE)
            label = self.font.render(button.label, True, colors.WHITE)
            self.screen.blit(label, label.get_rect(center=button.rect.center))

    def _draw_text(self, text, pos):
        self.screen.blit(self.font.render(text, True, colors.WHITE), pos)

    def _draw_centered(self, text, font, color, y):
        surface = font.render(text, True, color)
        self.screen.blit(surface, (WIDTH // 2 - surface.get_width() // 2, y))
