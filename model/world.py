from enum import Enum, auto

import math

from config import (
    WIDTH, HEIGHT, PLAYER_SIZE, TOTAL_WAVES, WAVE_PAUSE, HEAL_PER_WAVE,
    GRID_CELL_SIZE, NEIGHBOR_RADIUS,
)
from model.combat import check_attack_hit
from model.entities import Player
from model.spatial_grid import UniformGrid
from model.waves import spawn_wave


class GameStatus(Enum):
    PLAYING = auto()
    GAME_OVER = auto()
    VICTORY = auto()


class World:
    def __init__(self):
        self.player = Player(WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT // 2 - PLAYER_SIZE // 2)
        self.wave = 1
        self.enemies = spawn_wave(self.wave)
        self.wave_in_progress = True
        self.wave_pause_timer = 0.0
        self.status = GameStatus.PLAYING
        self._grid = UniformGrid(GRID_CELL_SIZE, WIDTH, HEIGHT)

    def move_player(self, dx, dy, dt):
        self.player.move(dx, dy, dt)

    def player_attack(self, aim_point):
        if not self.player.attack():
            return
        check_attack_hit(self.player, self.enemies, aim_point)
        self.enemies = [enemy for enemy in self.enemies if enemy.is_alive]

    def update(self, dt):
        if self.status is not GameStatus.PLAYING:
            return
        self.player.update(dt)
        self._update_enemies(dt)
        if not self.player.is_alive:
            self.status = GameStatus.GAME_OVER
            return
        self._update_waves(dt)

    def _update_enemies(self, dt):
        self._rebuild_grid()
        for enemy in self.enemies:
            enemy.update(dt, self.player.center, self._neighbors_of(enemy))
            if enemy.overlaps(self.player):
                self.player.take_damage(enemy.center)

    def _rebuild_grid(self):
        self._grid.clear()
        for enemy in self.enemies:
            cx, cy = enemy.center
            self._grid.insert(enemy, cx, cy)

    def _neighbors_of(self, enemy):
        cx, cy = enemy.center
        return [other for other in self._grid.query(cx, cy, NEIGHBOR_RADIUS)
                if other is not enemy and math.dist((cx, cy), other.center) < NEIGHBOR_RADIUS]

    def _update_waves(self, dt):
        if self.wave_in_progress:
            if not self.enemies:
                self.wave_in_progress = False
                self.wave_pause_timer = WAVE_PAUSE
            return
        self.wave_pause_timer -= dt
        if self.wave_pause_timer <= 0:
            self._start_next_wave()

    def _start_next_wave(self):
        if self.wave >= TOTAL_WAVES:
            self.status = GameStatus.VICTORY
            return
        self.wave += 1
        self.enemies = spawn_wave(self.wave)
        self.wave_in_progress = True
        self.player.heal(HEAL_PER_WAVE)
