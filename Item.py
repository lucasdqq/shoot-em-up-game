import pygame
from os.path import join as path_join
from Colisao import Collider
from Player import Player
from Vector2 import Vector2
from Ambiente import GAME_ZONE, music_module

class Item:
    def __init__(self, position: Vector2, sprite: pygame.Surface, collider: Collider, on_collect: callable, homing: bool = False):
        self._position = position
        self._start_position = position
        self._sprite = sprite
        self._collider = collider
        self._on_collect = on_collect
        self._homing = homing
        self._t = -10

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: Vector2):
        self._position = value

    @property
    def start_position(self):
        return self._start_position

    @start_position.setter
    def start_position(self, value: Vector2):
        self._start_position = value

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, value: pygame.Surface):
        self._sprite = value

    @property
    def collider(self):
        return self._collider

    @collider.setter
    def collider(self, value: Collider):
        self._collider = value

    @property
    def on_collect(self):
        return self._on_collect

    @on_collect.setter
    def on_collect(self, value: callable):
        self._on_collect = value

    @property
    def homing(self):
        return self._homing

    @homing.setter
    def homing(self, value: bool):
        self._homing = value

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, value: float):
        self._t = value

    def move(self, delta_time, player: Player) -> bool:
        if not self._homing:
            self._t += 10 * delta_time
            self._position = Vector2(self._start_position.x(), self._start_position.y() + (self._t ** 2 - 100))
        else:
            self._t += 60 * delta_time
            if self._t > 1.5:
                player_pos = player.position
                direction = player_pos - self._position
                self._position += direction.normalize() * 500 * delta_time

        self._collider.position = self._position
        if self._position.y() > GAME_ZONE[1] + GAME_ZONE[3]:
            del self
            return False
        return True

    def get_sprite(self) -> pygame.sprite.Sprite:
        sprite = pygame.sprite.Sprite()
        sprite.image = self._sprite
        sprite.rect = self._sprite.get_rect()
        sprite.rect.center = self._position.to_tuple()

        return sprite


class PowerItem(Item):
    def __init__(self, position: Vector2, large: bool, homing: bool = False):
        if large:
            sprite = pygame.image.load(path_join("assets", "sprites", "projectiles_and_items", "power_item_large.png"))
            collider = Collider(12)
            on_collect = self.on_collect_large
        else:
            sprite = pygame.image.load(path_join("assets", "sprites", "projectiles_and_items", "power_item_small.png"))
            collider = Collider(10)
            on_collect = self.on_collect_small

        super().__init__(position, sprite, collider, on_collect, homing)

    def on_collect_large(self, player: Player):
        music_module.sounds[20](.1)
        player.add_power(0.02)
        player.points += 10

    def on_collect_small(self, player: Player):
        music_module.sounds[20](.2)
        player.add_power(0.005)
        player.points += 10


class PointItem(Item):
    def __init__(self, position: Vector2, homing: bool = False):
        sprite = pygame.image.load(path_join("assets", "sprites", "projectiles_and_items", "point_item.png"))
        collider = Collider(10)
        on_collect = self.on_collect

        super().__init__(position, sprite, collider, on_collect, homing)

    def on_collect(self, player: Player):
        player.points += 30000 + int(70000 * (GAME_ZONE[3] + GAME_ZONE[1] - self._position.y()) / GAME_ZONE[3])


class StarItem(Item):
    def __init__(self, position: Vector2):
        sprite = pygame.image.load(path_join("assets", "sprites", "projectiles_and_items", "star_item.png"))
        collider = Collider(10)
        on_collect = self.on_collect

        super().__init__(position, sprite, collider, on_collect, True)

    def on_collect(self, player: Player):
        player.points += 200
