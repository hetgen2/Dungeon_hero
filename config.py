
#Окно
WIDTH = 1920
HEIGHT = 1080
FPS = 60
CAPTION = "DUNGEON HERO"
MAX_FRAME_TIME = 0.05 

#Игрок
PLAYER_SIZE = 50
PLAYER_MAX_HP = 5
PLAYER_SPEED = 480
PLAYER_DAMAGE = 1
PLAYER_INVINCIBLE_TIME = 0.67   
PLAYER_HIT_PUSHBACK = 50        
#Атака игрока
ATTACK_DURATION = 0.13
ATTACK_COOLDOWN = 0.42
ATTACK_DISTANCE = 120
ATTACK_HALF_ANGLE_DEG = 60

#Враги
ENEMY_SIZE = 45
BOSS_SIZE = 80
KNOCKBACK_DURATION = 0.17
KNOCKBACK_SPEED = 720

#Steering и стая (Boids)
ENEMY_MAX_FORCE = 1500           
STEERING_GAIN = 8.0              
SEEK_WEIGHT = 1.0
SEPARATION_WEIGHT = 1.5          
SEPARATION_RADIUS = 50
ALIGNMENT_WEIGHT = 0.1
ALIGNMENT_RADIUS = 30
COHESION_WEIGHT = 0.2
COHESION_RADIUS = 60
NEIGHBOR_RADIUS = max(SEPARATION_RADIUS, ALIGNMENT_RADIUS, COHESION_RADIUS)
GRID_CELL_SIZE = 100             

ENEMY_STATS = {
    "slime":    {"hp": 1,  "speed": 210, "size": ENEMY_SIZE, "show_hp": False, "knockbackable": True},
    "skeleton": {"hp": 2,  "speed": 300, "size": ENEMY_SIZE, "show_hp": True,  "knockbackable": True},
    "knight":   {"hp": 3,  "speed": 180, "size": ENEMY_SIZE, "show_hp": True,  "knockbackable": True},
    "ghost":    {"hp": 2,  "speed": 240, "size": ENEMY_SIZE, "show_hp": True,  "knockbackable": True},
    "boss":     {"hp": 12, "speed": 150, "size": BOSS_SIZE,  "show_hp": False, "knockbackable": False},
}

#Босс
BOSS_CHARGE_TIME = 0.42          
BOSS_DASH_TIME = 0.33            
BOSS_DASH_SPEED = 1080
BOSS_DASH_CHANCE = 0.25          
BOSS_DASH_CHECK_INTERVAL = 0.5   

SPAWN_AREAS = {
    "right": (WIDTH // 2 + 150, WIDTH - 150, 80, HEIGHT - 80),
    "center": (WIDTH // 4, WIDTH - WIDTH // 4, 80, HEIGHT - 80),
    "boss_spawn": (
        WIDTH // 2 - BOSS_SIZE // 2, WIDTH // 2 - BOSS_SIZE // 2,
        HEIGHT // 2 - BOSS_SIZE // 2, HEIGHT // 2 - BOSS_SIZE // 2,
    ),
}

#Волны
WAVE_PAUSE = 1.0
HEAL_PER_WAVE = 1
WAVES = [
    [("slime", 5, "right")],
    [("slime", 5, "right"), ("skeleton", 4, "right")],
    [("slime", 5, "right"), ("skeleton", 5, "right"), ("knight", 5, "right")],
    [("ghost", 4, "center"), ("boss", 1, "boss_spawn")],
]
TOTAL_WAVES = len(WAVES)
