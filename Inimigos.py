import numpy as np
import pygame.surface

from LimpaTela import BulletCleaner
from Efeitos import Effect
from Item import *
from Sprites import SpriteSheet
from Vector2 import Vector2
from Entidades import Entity
from Ambiente import music_module
from Funcoes import scale_sprite, set_alpha_sprite
from Splines import BasisSpline

BSpline = BasisSpline()

class Enemy(Entity):
    def __init__(self,
                 position: Vector2,
                 trajectory: [np.ndarray, ...],
                 speed,
                 sprite_sheet: SpriteSheet,
                 collider: Collider,
                 hp: int,
                 attack_data: [(callable, float), ...],
                 drop,
                 clear_bullets_on_death,
                 bullet_pool,
                 scene):

        super().__init__()
        self._start_position: Vector2 = position
        self._position: Vector2 = position
        self._trajectory = trajectory
        self._t = 0

        self._max_hp: int = hp
        self._current_hp: int = self._max_hp

        self._attack_data: [(callable, float), ...] = attack_data
        self._attack_count = 0

        self._sprite_sheet = sprite_sheet
        self._current_sprite = 0
        self._change_sprite_timer = 10

        self._death_effect_sprite = pygame.sprite.Sprite()
        self._death_effect_sprite.image = pygame.image.load(path_join("assets", "sprites", "effects", "fairy_death_0.png")).convert_alpha()
        self._death_effect_sprite.rect = self._death_effect_sprite.image.get_rect()

        self._bullet_spawn_sprite = pygame.sprite.Sprite()
        self._bullet_spawn_sprite.image = pygame.image.load(path_join("assets", "sprites", "effects", "bullet_spawn_effect.png")).convert_alpha()
        self._bullet_spawn_sprite.rect = self._bullet_spawn_sprite.image.get_rect()

        self._clear_bullets_on_death = clear_bullets_on_death

        self._bullets: list = bullet_pool

        self._collider: Collider = collider
        self._drop = drop

        self._scene = scene
        self._target = scene.player

        self._speed = speed

    @property
    def start_position(self) -> Vector2:
        return self._start_position

    @start_position.setter
    def start_position(self, value: Vector2) -> None:
        self._start_position = value

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, value: Vector2) -> None:
        self._position = value

    @property
    def trajectory(self) -> [np.ndarray, ...]:
        return self._trajectory

    @trajectory.setter
    def trajectory(self, value: [np.ndarray, ...]) -> None:
        self._trajectory = value

    @property
    def t(self) -> float:
        return self._t

    @t.setter
    def t(self, value: float) -> None:
        self._t = value

    @property
    def max_hp(self) -> int:
        return self._max_hp

    @max_hp.setter
    def max_hp(self, value: int) -> None:
        self._max_hp = value

    @property
    def current_hp(self) -> int:
        return self._current_hp

    @current_hp.setter
    def current_hp(self, value: int) -> None:
        self._current_hp = value

    @property
    def attack_data(self) -> [(callable, float), ...]:
        return self._attack_data

    @attack_data.setter
    def attack_data(self, value: [(callable, float), ...]) -> None:
        self._attack_data = value

    @property
    def attack_count(self) -> int:
        return self._attack_count

    @attack_count.setter
    def attack_count(self, value: int) -> None:
        self._attack_count = value

    @property
    def sprite_sheet(self) -> SpriteSheet:
        return self._sprite_sheet

    @sprite_sheet.setter
    def sprite_sheet(self, value: SpriteSheet) -> None:
        self._sprite_sheet = value

    @property
    def current_sprite(self) -> int:
        return self._current_sprite

    @current_sprite.setter
    def current_sprite(self, value: int) -> None:
        self._current_sprite = value

    @property
    def change_sprite_timer(self) -> int:
        return self._change_sprite_timer

    @change_sprite_timer.setter
    def change_sprite_timer(self, value: int) -> None:
        self._change_sprite_timer = value

    @property
    def death_effect_sprite(self) -> pygame.sprite.Sprite:
        return self._death_effect_sprite

    @death_effect_sprite.setter
    def death_effect_sprite(self, value: pygame.sprite.Sprite) -> None:
        self._death_effect_sprite = value

    @property
    def bullet_spawn_sprite(self) -> pygame.sprite.Sprite:
        return self._bullet_spawn_sprite

    @bullet_spawn_sprite.setter
    def bullet_spawn_sprite(self, value: pygame.sprite.Sprite) -> None:
        self._bullet_spawn_sprite = value

    @property
    def clear_bullets_on_death(self) -> bool:
        return self._clear_bullets_on_death

    @clear_bullets_on_death.setter
    def clear_bullets_on_death(self, value: bool) -> None:
        self._clear_bullets_on_death = value

    @property
    def bullets(self) -> list:
        return self._bullets

    @bullets.setter
    def bullets(self, value: list) -> None:
        self._bullets = value

    @property
    def collider(self) -> Collider:
        return self._collider

    @collider.setter
    def collider(self, value: Collider) -> None:
        self._collider = value

    @property
    def drop(self):
        return self._drop

    @drop.setter
    def drop(self, value) -> None:
        self._drop = value

    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, value) -> None:
        self._scene = value

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value) -> None:
        self._target = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value) -> None:
        self._speed = value

    def move(self) -> None:
        self.collider.position = self.position + self.collider.offset
        delta_time = self.scene.delta_time
        self.position = Vector2(coords=BSpline.curve(self.trajectory, self.t)) + Vector2(GAME_ZONE[0], GAME_ZONE[1])
        self.t += self.speed * delta_time
        if self.t > len(self.trajectory) - 1:
            self.death()

    def update(self) -> None:
        self.change_sprite_timer += 1 * 60 * self.scene.delta_time

        if self.attack_data and self.attack_count < len(self.attack_data):
            if self.t >= self.attack_data[self.attack_count][1]:
                music_module.sounds[3](.1)
                bullets = self.attack_data[self.attack_count][0](*self.attack_data[self.attack_count][2])

                for bullet in bullets:
                    bullet.position += self.position

                if len(self.bullets) > 0:
                    self.scene.effects.append(Effect(
                        position=bullets[0].position,
                        sprite_sheet=[set_alpha_sprite(scale_sprite(self.bullet_spawn_sprite, 3 - n / 2), 50 + n * 41).image for n in range(5)],
                        delay=4
                    ))

                self.bullets.extend(bullets)
                self.attack_count += 1

        self.next_sprite(4)

        for bullet in self.target.bullets:
            if self.collider.check_collision(bullet.collider):
                self.target.points += 100
                self.get_damage(bullet.damage)
                self.target.bullets.remove(bullet)
                del bullet

    def get_damage(self, damage: int) -> None:
        music_module.sounds[2](.2)
        self.current_hp -= damage
        if self.current_hp <= 0:
            self.death()

    def death(self):
        if self.current_hp <= 0:
            music_module.sounds[23](.15)

            if self.clear_bullets_on_death:
                self.scene.bullet_cleaner = BulletCleaner(self.position, give_points=True, show_sprite=False, increase_speed=2000)

            self.scene.effects.append(Effect(
                position=self.position,
                sprite_sheet=[set_alpha_sprite(scale_sprite(self.death_effect_sprite, 1 + n / 2), 255 - n * 51).image for n in range(5)],
                delay=4
            ))

            self.target.points += 10000
            drops = np.random.choice(self.drop[0], np.random.randint(1, 4), self.drop[1])
            drop_item = None
            for drop in drops:
                if drop == "power_large":
                    drop_item = PowerItem(self.position + Vector2.random_int(-75, 75, -50, 0), True)
                elif drop == "power_small":
                    drop_item = PowerItem(self.position + Vector2.random_int(-75, 75, -50, 0), False)
                elif drop == "points":
                    drop_item = PointItem(self.position + Vector2.random_int(-75, 75, -50, 0))


                if drop_item is not None:
                    self.scene.items.append(drop_item)

        if self in self.scene.enemies:
            self.scene.enemies.remove(self)
        del self
