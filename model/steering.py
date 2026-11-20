import math

from config import (
    STEERING_GAIN, SEEK_WEIGHT, SEPARATION_WEIGHT, SEPARATION_RADIUS, ALIGNMENT_WEIGHT,
    ALIGNMENT_RADIUS, COHESION_WEIGHT, COHESION_RADIUS,
)
from utils import clamp_magnitude, normalize

ZERO = (0.0, 0.0)


def _steer(direction, vel, max_speed, max_force):#тут задает инерцую
    desired_x = direction[0] * max_speed
    desired_y = direction[1] * max_speed
    return clamp_magnitude((desired_x - vel[0]) * STEERING_GAIN,
                           (desired_y - vel[1]) * STEERING_GAIN, max_force)


def seek(pos, vel, target, max_speed, max_force):#прсто направление
    direction = normalize(target[0] - pos[0], target[1] - pos[1])
    return _steer(direction, vel, max_speed, max_force)


def separation(pos, vel, neighbors, radius, max_speed, max_force):#толкучка
    sum_x = sum_y = 0.0
    count = 0
    for other in neighbors:
        dx = pos[0] - other.center[0]
        dy = pos[1] - other.center[1]
        dist = math.hypot(dx, dy)
        if 0 < dist < radius:
            sum_x += dx / dist / dist#делим 2 раза чтобы чем бдиже тем сильнеее
            sum_y += dy / dist / dist
            count += 1
    if count == 0:
        return ZERO
    direction = normalize(sum_x / count, sum_y / count)
    return _steer(direction, vel, max_speed, max_force)


def alignment(pos, vel, neighbors, radius, max_speed, max_force):#просто выравнивание скорости
    sum_x = sum_y = 0.0
    count = 0
    for other in neighbors:
        if math.dist(pos, other.center) < radius:
            sum_x += other.vel[0]
            sum_y += other.vel[1]
            count += 1
    if count == 0:
        return ZERO
    direction = normalize(sum_x / count, sum_y / count)
    return _steer(direction, vel, max_speed, max_force)


def cohesion(pos, vel, neighbors, radius, max_speed, max_force):#стадо    
    sum_x = sum_y = 0.0
    count = 0
    for other in neighbors:
        if math.dist(pos, other.center) < radius:
            sum_x += other.center[0]#сумма центров
            sum_y += other.center[1]
            count += 1
    if count == 0:
        return ZERO
    centroid = (sum_x / count, sum_y / count)
    return seek(pos, vel, centroid, max_speed, max_force)


def chase_in_flock(pos, vel, target, neighbors, max_speed, max_force):#итог
    forces = [
        (seek(pos, vel, target, max_speed, max_force), SEEK_WEIGHT),
        (separation(pos, vel, neighbors, SEPARATION_RADIUS, max_speed, max_force), SEPARATION_WEIGHT),
        (alignment(pos, vel, neighbors, ALIGNMENT_RADIUS, max_speed, max_force), ALIGNMENT_WEIGHT),
        (cohesion(pos, vel, neighbors, COHESION_RADIUS, max_speed, max_force), COHESION_WEIGHT),
    ]
    total_x = 0
    for force, weight in forces:
        total_x+=force[0]*weight
    total_y = 0
    for force, weight in forces:
        total_y+=force[1]*weight
    
    return clamp_magnitude(total_x, total_y, max_force)
