import random


def _expected_trials(c):#сколько попытко нужно
    expected = 0.0
    survive = 1.0#прошлые попытки неудачные
    n = 1
    while True:
        chance = min(1.0, n * c)
        expected += n * survive * chance# это шанс что успех именно здесь умножается на номер трая и я нахожу среднее
        survive *= 1 - chance# тут уменьшается шанс того что прошлые бросики ьыои неудачными
        if chance >= 1.0:
            return expected
        n += 1


def prd_constant(nominal_chance):#c ищу
    if nominal_chance <= 0:
        return 0.0
    if nominal_chance >= 1:
        return 1.0
    low, high = 0.0, nominal_chance
    for _ in range(60):
        mid = (low + high) / 2
        if _expected_trials(mid) > 1 / nominal_chance:#слишком медленно
            low = mid  
        else:
            high = mid#наоборот
    return (low + high) / 2


class PseudoRandomChance:
    def __init__(self, nominal_chance, rng=random.random):
        self.c = prd_constant(nominal_chance)
        self.current_chance = self.c
        self._rng = rng

    def check(self):
        if self._rng() < self.current_chance:
            self.current_chance = self.c    
            return True
        self.current_chance += self.c      
        return False
