import math


def clamp(value, low, high):
    return max(low, min(high, value))


def normalize(dx, dy):
    length = math.hypot(dx, dy)
    if length == 0:
        return 0.0, 0.0
    return dx / length, dy / length


def clamp_magnitude(x, y, max_length):
    length = math.hypot(x, y)
    if length <= max_length or length == 0:
        return x, y
    scale = max_length / length
    return x * scale, y * scale
