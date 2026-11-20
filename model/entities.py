from config import (
    WIDTH, HEIGHT, PLAYER_SIZE, PLAYER_MAX_HP, PLAYER_SPEED, PLAYER_DAMAGE,
    PLAYER_INVINCIBLE_TIME, PLAYER_HIT_PUSHBACK, ATTACK_DURATION, ATTACK_COOLDOWN,
    ENEMY_STATS, KNOCKBACK_DURATION, KNOCKBACK_SPEED, ENEMY_MAX_FORCE,
)
from model.steering import chase_in_flock, seek
from utils import clamp, clamp_magnitude, normalize


class Entity:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def center(self):
        return self.x + self.width / 2, self.y + self.height / 2

    def overlaps(self, other):
        return (self.x < other.x + other.width and other.x < self.x + self.width
                and self.y < other.y + other.height and other.y < self.y + self.height)

    def clamp_to_screen(self):
        self.x = clamp(self.x, 0, WIDTH - self.width)
        self.y = clamp(self.y, 0, HEIGHT - self.height)

    def move_by(self, dx, dy):
        self.x += dx
        self.y += dy
        self.clamp_to_screen()


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.max_hp = PLAYER_MAX_HP
        self.hp = PLAYER_MAX_HP
        self.damage = PLAYER_DAMAGE
        self.invincible_timer = 0.0
        self.attack_timer = 0.0
        self.attack_cooldown = 0.0

    @property
    def is_alive(self):
        return self.hp > 0

    @property
    def is_invincible(self):
        return self.invincible_timer > 0

    @property
    def is_attacking(self):
        return self.attack_timer > 0

    def move(self, dx, dy, dt):
        dir_x, dir_y = normalize(dx, dy)
        self.move_by(dir_x * PLAYER_SPEED * dt, dir_y * PLAYER_SPEED * dt)

    def attack(self):
        if self.attack_cooldown > 0:
            return False
        self.attack_timer = ATTACK_DURATION
        self.attack_cooldown = ATTACK_COOLDOWN
        return True

    def take_damage(self, source_center):
        if self.is_invincible:
            return False
        self.hp -= 1
        self.invincible_timer = PLAYER_INVINCIBLE_TIME
        cx, cy = self.center
        dir_x, dir_y = normalize(cx - source_center[0], cy - source_center[1])
        self.move_by(dir_x * PLAYER_HIT_PUSHBACK, dir_y * PLAYER_HIT_PUSHBACK)
        return True

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def update(self, dt):
        self.invincible_timer = max(0.0, self.invincible_timer - dt)
        self.attack_timer = max(0.0, self.attack_timer - dt)
        self.attack_cooldown = max(0.0, self.attack_cooldown - dt)


class Enemy(Entity):
    
    def __init__(self, x, y, kind):
        stats = ENEMY_STATS[kind]
        super().__init__(x, y, stats["size"], stats["size"])
        self.kind = kind
        self.max_hp = stats["hp"]
        self.hp = stats["hp"]
        self.speed = stats["speed"]
        self.show_hp = stats["show_hp"]
        self.knockbackable = stats["knockbackable"]
        self.vel = (0.0, 0.0)
        self.knockback_timer = 0.0
        self.knockback_dir = (0.0, 0.0)

    @property
    def is_alive(self):
        return self.hp > 0

    def take_hit(self, damage, source_center):
        self.hp -= damage
        if self.knockbackable:
            cx, cy = self.center
            self.knockback_dir = normalize(cx - source_center[0], cy - source_center[1])
            self.knockback_timer = KNOCKBACK_DURATION
            self.vel = (0.0, 0.0)

    def update(self, dt, target, neighbors=()):
        if self._apply_knockback(dt):
            return
        force = chase_in_flock(self.center, self.vel, target, neighbors,
                               self.speed, ENEMY_MAX_FORCE)
        self._apply_force(force, dt)

    def _apply_knockback(self, dt):
        if self.knockback_timer <= 0:
            return False
        self.knockback_timer -= dt
        dir_x, dir_y = self.knockback_dir
        self.move_by(dir_x * KNOCKBACK_SPEED * dt, dir_y * KNOCKBACK_SPEED * dt)
        return True

    def _steer_towards(self, target, dt):
        force = seek(self.center, self.vel, target, self.speed, ENEMY_MAX_FORCE)
        self._apply_force(force, dt)

    def _apply_force(self, force, dt):
        vx = self.vel[0] + force[0] * dt
        vy = self.vel[1] + force[1] * dt
        self.vel = clamp_magnitude(vx, vy, self.speed)
        self.move_by(self.vel[0] * dt, self.vel[1] * dt)
