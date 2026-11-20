import random
from config import WAVES, SPAWN_AREAS
from model.boss import Boss
from model.entities import Enemy


def create_enemy(kind, x, y):
    if kind == "boss":
        return Boss(x, y)
    return Enemy(x, y, kind)


def spawn_wave(wave_number):
    enemies = []
    for kind, count, area in WAVES[wave_number - 1]:
        x_min, x_max, y_min, y_max = SPAWN_AREAS[area]
        for _ in range(count):
            x = random.randint(x_min, x_max)
            y = random.randint(y_min, y_max)
            enemies.append(create_enemy(kind, x, y))
    return enemies
