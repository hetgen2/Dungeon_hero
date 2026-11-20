from enum import Enum, auto

import pygame

from config import WIDTH, HEIGHT, FPS, CAPTION, MAX_FRAME_TIME
from model.world import GameStatus, World
from view import colors
from view.renderer import Renderer
from view.screens import MENU_BUTTONS, GAME_OVER_BUTTONS, VICTORY_BUTTONS


class AppState(Enum):
    MENU = auto()
    PLAYING = auto()
    GAME_OVER = auto()
    VICTORY = auto()
    EXIT = auto()


BUTTONS_BY_STATE = {
    AppState.MENU: MENU_BUTTONS,
    AppState.GAME_OVER: GAME_OVER_BUTTONS,
    AppState.VICTORY: VICTORY_BUTTONS,
}


class Game:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        self.renderer = Renderer(screen)
        self.state = AppState.MENU
        self.world = None

    def run(self):
        while self.state is not AppState.EXIT:
            dt = min(self.clock.tick(FPS) / 1000, MAX_FRAME_TIME)
            self._handle_events()
            self._update(dt)
            self._render()
        pygame.quit()


    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = AppState.EXIT
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(event.pos)

    def _handle_click(self, pos):
        if self.state is AppState.PLAYING:
            self.world.player_attack(pos)
            return
        for button in BUTTONS_BY_STATE.get(self.state, []):
            if button.contains(pos):
                self._run_action(button.action)
                return

    def _run_action(self, action):
        if action == "start":
            self.world = World()
            self.state = AppState.PLAYING
        elif action == "menu":
            self.state = AppState.MENU
        elif action == "exit":
            self.state = AppState.EXIT

    @staticmethod
    def _read_move_direction():
        keys = pygame.key.get_pressed()
        dx = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        dy = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        return dx, dy

    def _update(self, dt):
        if self.state is not AppState.PLAYING:
            return
        dx, dy = self._read_move_direction()
        self.world.move_player(dx, dy, dt)
        self.world.update(dt)
        if self.world.status is GameStatus.GAME_OVER:
            self.state = AppState.GAME_OVER
        elif self.world.status is GameStatus.VICTORY:
            self.state = AppState.VICTORY

    def _render(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.state is AppState.PLAYING:
            self.renderer.draw_world(self.world, mouse_pos)
        elif self.state is AppState.MENU:
            self.renderer.draw_menu(MENU_BUTTONS, mouse_pos)
        elif self.state is AppState.GAME_OVER:
            self.renderer.draw_end_screen("GAME OVER", colors.RED, None, GAME_OVER_BUTTONS, mouse_pos)
        elif self.state is AppState.VICTORY:
            self.renderer.draw_end_screen("ПОБЕДА!", colors.GREEN, "Ты убил босса!", VICTORY_BUTTONS, mouse_pos)
        pygame.display.flip()
