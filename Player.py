import pygame.transform
from LimpaTela import BulletCleaner
from Entidades import Entity
from DadosPersonagens import *
from Vector2 import Vector2
from Funcoes import *
from Ambiente import *

class Player(Entity):
    def __init__(self, id: int, scene, hp: int):
        super().__init__()
        self._name: str = characters[id]['name']
        self._sprite_sheet: pygame.sprite = characters[id]['sprite-sheet']
        self._attack_function: callable = characters[id]['attack-function']

        self._position: Vector2 = Vector2((GAME_ZONE[2] + GAME_ZONE[0] + self._sprite_sheet.x) // 2, GAME_ZONE[1] + GAME_ZONE[3] - 100)
        self._speed: int = characters[id]['speed']

        self._collider = Collider(3)

        self._hitbox_sprite = pygame.image.load(path_join("assets", "sprites", "effects", "player_hitbox.png")).convert_alpha()
        self._hitbox_sprites = [pygame.transform.rotate(self._hitbox_sprite, n) for n in range(360)]
        self._change_hitbox_sprite_timer = 0

        self._default_sprites = [self._sprite_sheet[i] for i in range(len(self._sprite_sheet))]
        self._right_slope_sprites = [pygame.transform.rotate(self._sprite_sheet[i], 7) for i in range(len(self._sprite_sheet))]
        self._left_slope_sprites = [pygame.transform.flip(sprite, flip_x=True, flip_y=False) for sprite in self._right_slope_sprites]

        self._points = 0
        self._hp = hp
        self._reviving = False
        self._invincibility_timer = 0

        self._sprite_size = Vector2(self._sprite_sheet.x, self._sprite_sheet.y)

        self._change_sprite_timer = 0
        self._slow: bool = False

        self._attack_timer = 0
        self._power = 2.4

        self._bullets = []

        self._slowRate = Vector2.zero()

        self._scene = scene

    @property
    def name(self):
        return self._name

    @property
    def sprite_sheet(self):
        return self._sprite_sheet

    @property
    def attack_function(self):
        return self._attack_function

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: Vector2):
        self._position = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value: int):
        self._speed = value

    @property
    def collider(self):
        return self._collider

    @collider.setter
    def collider(self, value: Collider):
        self._collider = value

    @property
    def hitbox_sprite(self):
        return self._hitbox_sprite

    @property
    def hitbox_sprites(self):
        return self._hitbox_sprites

    @property
    def change_hitbox_sprite_timer(self):
        return self._change_hitbox_sprite_timer

    @change_hitbox_sprite_timer.setter
    def change_hitbox_sprite_timer(self, value: float):
        self._change_hitbox_sprite_timer = value

    @property
    def default_sprites(self):
        return self._default_sprites

    @property
    def right_slope_sprites(self):
        return self._right_slope_sprites

    @property
    def left_slope_sprites(self):
        return self._left_slope_sprites

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value: int):
        self._points = value

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value: int):
        self._hp = value

    @property
    def reviving(self):
        return self._reviving

    @reviving.setter
    def reviving(self, value: bool):
        self._reviving = value

    @property
    def invincibility_timer(self):
        return self._invincibility_timer

    @invincibility_timer.setter
    def invincibility_timer(self, value: float):
        self._invincibility_timer = value

    @property
    def sprite_size(self):
        return self._sprite_size

    @property
    def change_sprite_timer(self):
        return self._change_sprite_timer

    @change_sprite_timer.setter
    def change_sprite_timer(self, value: float):
        self._change_sprite_timer = value

    @property
    def slow(self):
        return self._slow

    @slow.setter
    def slow(self, value: bool):
        self._slow = value

    @property
    def attack_timer(self):
        return self._attack_timer

    @attack_timer.setter
    def attack_timer(self, value: float):
        self._attack_timer = value

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, value: float):
        self._power = value

    @property
    def bullets(self):
        return self._bullets

    @bullets.setter
    def bullets(self, value: list):
        self._bullets = value

    @property
    def slowRate(self):
        return self._slowRate

    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, value):
        self._scene = value

    def update(self) -> None:
        delta_time = self._scene.delta_time

        if self._slow:
            self._slowRate += Vector2.one() * delta_time
        else:
            self._slowRate += Vector2.right() * delta_time

        if not self._reviving:
            for bullet in self._scene.enemy_bullets:
                if bullet.collider.check_collision(self._collider):
                    self.get_damage()
                    break

            for enemy in self._scene.enemies:
                if enemy.collider.check_collision(self._collider):
                    self.get_damage()
                    break

        for item in self._scene.items:
            if item.collider.check_collision(self._collider):
                item.on_collect(self)
                music_module.sounds[8](.1)
                self._scene.items.remove(item)
                del item

        self._attack_timer += 2.5 * 60 * delta_time
        self._change_sprite_timer += 1 * 60 * delta_time
        self._change_hitbox_sprite_timer += 1 * 60 * delta_time
        self.next_sprite(5)

    def move(self, direction_vector: Vector2) -> None:
        sprite_rect = self.get_sprite().rect

        self._sprite_sheet = self._default_sprites \
            if direction_vector.x() == 0\
            else self._right_slope_sprites if direction_vector.x() < 0\
            else self._left_slope_sprites

        delta_time = self._scene.delta_time

        if self._reviving:
            self._invincibility_timer += 1 * 60 * delta_time
            self._position += Vector2.up() * 2 * 60 * delta_time

            # If no HP left
            if self._hp < 0 and self._position.y() <= GAME_ZONE[3] + GAME_ZONE[1] + 40:
                self.switch_to_scoreboard()

            if self._position.y() <= GAME_ZONE[3] + GAME_ZONE[1] - 100:
                self._reviving = False
                self._invincibility_timer = 0
        else:
            self._position = (self._position + direction_vector.normalize() * self._speed * delta_time * (.5 if self._slow else 1)) \
                .clamp(GAME_ZONE[0] + sprite_rect.w // 2, (GAME_ZONE[2] + GAME_ZONE[0]) - sprite_rect.w // 2,
                       GAME_ZONE[1] + sprite_rect.h // 2, (GAME_ZONE[3] + GAME_ZONE[1]) - sprite_rect.h // 2)

        self._collider.position = self._position

    def shoot(self) -> None:
        if self._attack_timer >= 16:
            music_module.sounds[17](.1)
            self._bullets += self._attack_function(self._position + Vector2.up() * 10, int(self._power))
            self._attack_timer = 0

    def get_damage(self):
        music_module.sounds[16](.2)
        self._scene.bullet_cleaner = BulletCleaner(self._position)
        self._hp -= 1
        self._reviving = True
        self._position = Vector2(50 + (GAME_ZONE[2] - GAME_ZONE[0]) // 2, HEIGHT + 80)

    def add_power(self, power: float):
        self._power += power
        if self._power > 4:
            self._power = 4

    def switch_to_scoreboard(self):
        from CenaRanking import ScoreboardScene
        self._scene.switch_to_scene(ScoreboardScene(self))

    def get_hitbox_sprite(self):
        return self._hitbox_sprites[clamp(int(self._change_hitbox_sprite_timer % 360), 0, len(self._hitbox_sprites) - 1)]
