from dataclasses import dataclass

import pygame


@dataclass(frozen=True)
class Button:
    label: str
    rect: pygame.Rect
    color: tuple
    hover_color: tuple
    action: str

    def contains(self, pos):
        return self.rect.collidepoint(pos)
