import random
from enum import Enum, auto

from config import (
    BOSS_CHARGE_TIME, BOSS_DASH_TIME, BOSS_DASH_SPEED,
    BOSS_DASH_CHANCE, BOSS_DASH_CHECK_INTERVAL,
)
from model.entities import Enemy
from model.random_tools import PseudoRandomChance
from utils import normalize


class BossState(Enum):
    CHASE = auto()     
    CHARGING = auto()  
    DASHING = auto()   


class Boss(Enemy):
    def __init__(self, x, y, rng=random.random):
        super().__init__(x, y, "boss")
        self.state = BossState.CHASE
        self.state_timer = 0.0
        self.dash_dir = (0.0, 0.0)
        self._dash_chance = PseudoRandomChance(BOSS_DASH_CHANCE, rng)
        self._check_timer = BOSS_DASH_CHECK_INTERVAL

    def update(self, dt, target, neighbors=()):
        if self.state is BossState.CHASE:
            self._update_chase(dt, target)
        elif self.state is BossState.CHARGING:
            self._update_charging(dt, target)
        else:
            self._update_dashing(dt)

    def _update_chase(self, dt, target):
        self._steer_towards(target, dt)
        self._check_timer -= dt
        if self._check_timer > 0:
            return
        self._check_timer += BOSS_DASH_CHECK_INTERVAL
        if self._dash_chance.check():
            self.state = BossState.CHARGING
            self.state_timer = BOSS_CHARGE_TIME
            self.vel = (0.0, 0.0)

    def _update_charging(self, dt, target):
        self.state_timer -= dt
        if self.state_timer <= 0:
            cx, cy = self.center
            self.dash_dir = normalize(target[0] - cx, target[1] - cy) 
            self.state = BossState.DASHING
            self.state_timer = BOSS_DASH_TIME

    def _update_dashing(self, dt):
        dir_x, dir_y = self.dash_dir
        self.move_by(dir_x * BOSS_DASH_SPEED * dt, dir_y * BOSS_DASH_SPEED * dt)
        self.state_timer -= dt
        if self.state_timer <= 0:
            self.state = BossState.CHASE
            self._check_timer = BOSS_DASH_CHECK_INTERVAL
