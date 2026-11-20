import math
from config import ATTACK_DISTANCE, ATTACK_HALF_ANGLE_DEG

def aim_angle(origin, point):
    return math.atan2(point[1] - origin[1], point[0] - origin[0])


def angle_difference(a, b):
    diff = abs(a - b)
    return min(diff, 2 * math.pi - diff)


def is_in_sector(origin, aim, target, max_distance, half_angle):
    
    dx = target[0] - origin[0]
    dy = target[1] - origin[1]
    if math.hypot(dx, dy) > max_distance:
        return False
    return angle_difference(aim, math.atan2(dy, dx)) <= half_angle


def check_attack_hit(player, enemies, aim_point):
    origin = player.center
    aim = aim_angle(origin, aim_point)
    half_angle = math.radians(ATTACK_HALF_ANGLE_DEG)
    hits = []
    for enemy in enemies:
        if is_in_sector(origin, aim, enemy.center, ATTACK_DISTANCE, half_angle):
            enemy.take_hit(player.damage, origin)
            hits.append(enemy)
    return hits
