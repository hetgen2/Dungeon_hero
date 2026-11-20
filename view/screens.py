import pygame

from config import WIDTH
from view import colors
from view.ui import Button

BUTTON_HEIGHT = 70


def _centered_button(label, y, width, color, hover_color, action):
    rect = pygame.Rect(WIDTH // 2 - width // 2, y, width, BUTTON_HEIGHT)
    return Button(label, rect, color, hover_color, action)


MENU_BUTTONS = [
    _centered_button("НАЧАТЬ ИГРУ", 450, 300, colors.GREEN, colors.DARK_GREEN, "start"),
    _centered_button("ВЫХОД", 560, 300, colors.RED, colors.DARK_RED, "exit"),
]
GAME_OVER_BUTTONS = [
    _centered_button("В ГЛАВНОЕ МЕНЮ", 500, 350, colors.BLUE, colors.DARK_BLUE, "menu"),
]
VICTORY_BUTTONS = [
    _centered_button("В ГЛАВНОЕ МЕНЮ", 500, 350, colors.BLUE, colors.DARK_BLUE, "menu"),
]
