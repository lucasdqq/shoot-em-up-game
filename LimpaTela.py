import pygame
from os.path import join as path_join
from Colisao import Collider
from Vector2 import Vector2
from Ambiente import *
from Funcoes import clamp

class BulletCleaner:
    def __init__(self, position: Vector2, increase_speed: int = 1000, give_points: bool = False, show_sprite: bool = True):
        self._collider = Collider(0, position)
        self._sprite = pygame.image.load(path_join("assets", "sprites", "effects", "player_death_effect.png")).convert_alpha()

        self._increase_speed = increase_speed
        self._give_points = give_points
        self._kill = False
        self._show_sprite = show_sprite

    @property
    def collider(self):
        return self._collider

    @collider.setter
    def collider(self, value: Collider):
        self._collider = value

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, value: pygame.Surface):
        self._sprite = value

    @property
    def increase_speed(self):
        return self._increase_speed

    @increase_speed.setter
    def increase_speed(self, value: int):
        self._increase_speed = value

    @property
    def give_points(self):
        return self._give_points

    @give_points.setter
    def give_points(self, value: bool):
        self._give_points = value

    @property
    def kill(self):
        return self._kill

    @kill.setter
    def kill(self, value: bool):
        self._kill = value

    @property
    def show_sprite(self):
        return self._show_sprite

    @show_sprite.setter
    def show_sprite(self, value: bool):
        self._show_sprite = value

    def update(self, bullets, scene, delta_time):
        self._collider.radius += self._increase_speed * delta_time

        i = 0
        while i < len(bullets):
            if bullets[i].collider.check_collision(self._collider):
                bullet = bullets.pop(i)
                if self._give_points:
                    point_item = self.spawn_point_item(bullet.position)
                    scene.items.append(point_item)
                del bullet
                i -= 1
            i += 1

        if self._collider.radius ** 2 >= GAME_ZONE[2] ** 2 + GAME_ZONE[3] ** 2:
            self._kill = True

    def get_sprite(self):
        if not self._show_sprite:
            return pygame.Surface((0, 0))
        image = pygame.transform.scale(self._sprite, (self._collider.radius * 2, self._collider.radius * 2))
        image.set_alpha(clamp(255 - self._collider.radius ** 2 / (GAME_ZONE[2] ** 2 + GAME_ZONE[3] ** 2) * 1000, 0, 255))

        return image

    def spawn_point_item(self, position: Vector2):
        from Item import StarItem
        return StarItem(position)
