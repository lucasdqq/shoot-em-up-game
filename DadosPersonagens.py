from os.path import join as path_join

from DadosPro import BulletData
from Colisao import Collider
from Sprites import SpriteSheet
from ProjetilPlayer import PlayerBullet
from Projetil import Vector2


def marisa_base_attack(fire_point: Vector2, power: int):
    bullets = []

    power_levels = [0, 1, 2, 3]
    delta_angle = 10

    current_power = power_levels[int((len(power_levels) - 1) * power * 20 / 100)]

    bullet_data = BulletData(characters[0]["bullet-sprite-sheet"], Collider(5, offset=Vector2.up() * 10))

    for i in range(-current_power, current_power + 1):
        i /= 2
        bullet_1 = PlayerBullet(bullet_data, fire_point - Vector2(6, 0), delta_angle * i, 900, damage=1)
        bullet_2 = PlayerBullet(bullet_data, fire_point + Vector2(6, 0), delta_angle * i, 900, damage=1)
        bullets.append(bullet_1)
        bullets.append(bullet_2)

    return bullets

def reimu_base_attack(fire_point: Vector2, power: int):
    bullets = []

    power_levels = [0, 1, 2, 3]
    delta_angle = 0

    current_power = power_levels[int((len(power_levels) - 1) * power * 25 / 100)]

    bullet_data = BulletData(characters[1]["bullet-sprite-sheet"], Collider(5, offset=Vector2.up() * 10))

    for i in range(-current_power, current_power + 1):
        i /= 2
        bullet_1 = PlayerBullet(bullet_data, fire_point - Vector2(6, 0), delta_angle * i, 900, damage=1)
        bullet_2 = PlayerBullet(bullet_data, fire_point + Vector2(6, 0), delta_angle * i, 900, damage=1)
        bullets.append(bullet_1)
        bullets.append(bullet_2)

    return bullets


characters = {
    0: {
        "name": "Marisa",
        "speed": 370,
        "sprite-sheet": SpriteSheet(path_join("assets", "sprites", "entities", "marisa.png")).crop((25, 50)),
        "bullet-sprite-sheet": SpriteSheet(path_join("assets", "sprites", "projectiles_and_items", "marisa_bullet.png")).crop((32, 32)),
        "attack-function": marisa_base_attack
    },
    1: {
        "name": "Reimu",
        "speed": 330,
        "sprite-sheet": SpriteSheet(path_join("assets", "sprites", "entities", "reimu.png")).crop((25, 50)),
        "bullet-sprite-sheet": SpriteSheet(path_join("assets", "sprites", "projectiles_and_items", "reimu_bullet.png")).crop((32, 32)),
        "attack-function": reimu_base_attack
    },
}
