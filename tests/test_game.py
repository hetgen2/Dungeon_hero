import random
import unittest
from types import SimpleNamespace

from config import BOSS_CHARGE_TIME, BOSS_DASH_CHECK_INTERVAL, BOSS_DASH_TIME, WAVE_PAUSE
from model.boss import Boss, BossState
from model.combat import check_attack_hit
from model.entities import Enemy, Player
from model.random_tools import PseudoRandomChance, prd_constant
from model.spatial_grid import UniformGrid
from model.steering import separation
from model.world import World


def enemy_at(x, y):
    enemy = Enemy(0, 0, "slime")
    enemy.x = x - enemy.width / 2
    enemy.y = y - enemy.height / 2
    return enemy


class Tests(unittest.TestCase):
    def test_sword(self):
        player = Player(500, 500)
        front = enemy_at(600, 525)
        back = enemy_at(450, 525)
        hits = check_attack_hit(player, [front, back], (900, 525))
        self.assertEqual(hits, [front])


    def test_prd(self):
        self.assertAlmostEqual(prd_constant(0.25), 0.0847, places=3)
        prd = PseudoRandomChance(0.25, rng=random.Random(1).random)
        hits = miss = longest = 0
        for _ in range(20000):
            if prd.check():
                hits += 1
                miss = 0
            else:
                miss += 1
                longest = max(longest, miss)
        self.assertAlmostEqual(hits / 20000, 0.25, delta=0.02)
        self.assertLessEqual(longest, int(1 / prd.c))


    def test_waves(self):
        world = World()
        world.player.hp = 3
        world.enemies = []
        world.update(0.016)
        world.update(WAVE_PAUSE + 0.016)
        self.assertEqual(world.wave, 2)
        self.assertEqual(world.player.hp, 4)


if __name__ == "__main__":
    unittest.main()