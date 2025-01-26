import numpy as np
import pygame
from pygame.locals import *
import json

from DadosPro import BulletData
from Inimigos import Enemy
from Item import *
from Player import Player
from Cenas import Scene, render_fps
from Sprites import SpriteSheet
from Vector2 import Vector2
from FuncoesAtaque import AttackFunctions

from Ambiente import *

from PIL import Image


class PhysicsEngine:
    def __init__(self):
        self._gravity = 9.81
        self._wind_speed = 5.0

    def apply_physics(self, entity):
        # Código para aplicar física à entidade
        pass


class SoundManager:
    def __init__(self):
        self._sound_effects = {}

    def play_sound(self, sound_name):
        # Código para tocar som
        pass


class GameScene(Scene, PhysicsEngine, SoundManager):
    def __init__(self, selected_character):
        Scene.__init__(self)
        PhysicsEngine.__init__(self)
        SoundManager.__init__(self)
        self._game_zone = tuple(map(int, os.getenv("GAME_ZONE").split(', ')))
        self._delta_time = 0.001

        self._background = Image.open(path_join("assets", "sprites", "backgrounds", "background.jpg")).convert("RGBA")
        self._background.paste(Image.new("RGBA", (self._game_zone[2], self._game_zone[3]), (255, 255, 255, 0)),
                              (self._game_zone[0], self._game_zone[1]))
        self._bg = pygame.sprite.Sprite()
        self._bg.rect = Rect(0, 0, WIDTH, HEIGHT)
        self._bg.image = pygame.image.fromstring(self._background.tobytes(), self._background.size, self._background.mode).convert_alpha()

        self._font = pygame.font.Font(path_join("assets", "fonte.ttf"), 36)

        self._player = Player(selected_character, self, 4)

        self._enemy_bullets = []
        self._items = []
        self._bullet_cleaner = None

        self._effects = []

        self._bullet_group = pygame.sprite.RenderPlain()
        self._item_group = pygame.sprite.RenderPlain()
        self._hud_group = pygame.sprite.RenderPlain()
        self._entity_group = pygame.sprite.RenderPlain()
        self._effect_group = pygame.sprite.RenderPlain()

        self._time = 0
        self._level = json.load(open(path_join("assets", "spawn_inimigos.json")))
        self._level_enemies = sorted(self._level["enemies"], key=lambda enemy: enemy["time"])
        self._enemy_count = 0

        self._enemies = []

    @property
    def game_zone(self):
        return self._game_zone

    @property
    def delta_time(self):
        return self._delta_time

    @delta_time.setter
    def delta_time(self, value):
        self._delta_time = value

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, value):
        self._background = value

    @property
    def bg(self):
        return self._bg

    @bg.setter
    def bg(self, value):
        self._bg = value

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        self._font = value

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, value):
        self._player = value

    @property
    def enemy_bullets(self):
        return self._enemy_bullets

    @enemy_bullets.setter
    def enemy_bullets(self, value):
        self._enemy_bullets = value

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        self._items = value

    @property
    def bullet_cleaner(self):
        return self._bullet_cleaner

    @bullet_cleaner.setter
    def bullet_cleaner(self, value):
        self._bullet_cleaner = value

    @property
    def effects(self):
        return self._effects

    @effects.setter
    def effects(self, value):
        self._effects = value

    @property
    def bullet_group(self):
        return self._bullet_group

    @bullet_group.setter
    def bullet_group(self, value):
        self._bullet_group = value

    @property
    def item_group(self):
        return self._item_group

    @item_group.setter
    def item_group(self, value):
        self._item_group = value

    @property
    def hud_group(self):
        return self._hud_group

    @hud_group.setter
    def hud_group(self, value):
        self._hud_group = value

    @property
    def entity_group(self):
        return self._entity_group

    @entity_group.setter
    def entity_group(self, value):
        self._entity_group = value

    @property
    def effect_group(self):
        return self._effect_group

    @effect_group.setter
    def effect_group(self, value):
        self._effect_group = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def level_enemies(self):
        return self._level_enemies

    @level_enemies.setter
    def level_enemies(self, value):
        self._level_enemies = value

    @property
    def enemy_count(self):
        return self._enemy_count

    @enemy_count.setter
    def enemy_count(self, value):
        self._enemy_count = value

    @property
    def enemies(self):
        return self._enemies

    @enemies.setter
    def enemies(self, value):
        self._enemies = value

    def process_input(self, events):
        for evt in events:
            if evt.type == QUIT:
                pygame.quit()

        move_direction = Vector2.zero()

        if pygame.key.get_pressed()[pygame.K_UP]:
            move_direction += Vector2.up()
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            move_direction += Vector2.down()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            move_direction += Vector2.left()
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            move_direction += Vector2.right()

        if pygame.key.get_pressed()[pygame.K_z]:
            self._player.shoot()

        self._player.move(move_direction)

        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            self._player.slow = True
        else:
            self._player.slow = False

    def update(self, delta_time):
        self._delta_time = delta_time
        self._time += delta_time

        if self._time >= self._level["length"]:
            self._player.switch_to_scoreboard()

        if self._level_enemies and self._enemy_count < len(self._level_enemies):
            if self._time >= self._level_enemies[self._enemy_count]["time"]:
                enemy_data = self._level_enemies[self._enemy_count]
                enemy = Enemy(
                    position=Vector2(self._game_zone[0], self._game_zone[1]) + Vector2(*enemy_data["start_position"]),
                    trajectory=list(map(np.array, [enemy_data["start_position"]]+ enemy_data["trajectory"])),
                    speed=enemy_data["speed"],
                    sprite_sheet=SpriteSheet(path_join(*enemy_data["sprite"]["path"])).crop(enemy_data["sprite"]["size"]),
                    collider=Collider(enemy_data["collider"]["radius"], offset=Vector2(*enemy_data["collider"]["offset"])),
                    hp=enemy_data["hp"],
                    attack_data=[(*attack[:3], (path_join(*attack[3][0]), attack[3][1], attack[3][2], attack[3][3], Vector2(*attack[3][4])), *attack[4:]) for attack in enemy_data["attacks"]],
                    drop=(enemy_data["drop"]["list"], enemy_data["drop"]["list"]),
                    clear_bullets_on_death=enemy_data["clear_on_death"],
                    bullet_pool=self._enemy_bullets,
                    scene=self
                )

                attack_data = []
                for i in range(len(enemy.attack_data)):
                    if enemy.attack_data[i][0] == "wide_ring":
                        _, bul_num, ring_num, bul_data, spd, s_time, delay, a_speed, d_angle, rand_cnt = \
                        enemy.attack_data[i]
                        attack_data.extend(
                        AttackFunctions.wide_ring
                            (
                                number_of_bullets=bul_num,
                                number_of_rings=ring_num,
                                bullet_data=BulletData(
                                    SpriteSheet(bul_data[0]).crop((bul_data[1], bul_data[2])),
                                    Collider(bul_data[3], bul_data[4])
                                ),
                                speed=spd,
                                start_time=s_time,
                                delay=delay,
                                angular_speed=a_speed,
                                delta_angle=d_angle,
                                rand_center=rand_cnt
                            )
                        )
                    elif enemy.attack_data[i][0] == "long_random":
                        _, bul_num, rand_num, bul_data, spd, s_time, delay, a_speed, rand_cnt = \
                        enemy.attack_data[i]
                        attack_data.extend(
                        AttackFunctions.long_random
                            (
                                number_of_bullets=bul_num,
                                number_of_randoms=rand_num,
                                bullet_data=BulletData(
                                    SpriteSheet(bul_data[0]).crop((bul_data[1], bul_data[2])),
                                    Collider(bul_data[3], bul_data[4])
                                ),
                                speed=spd,
                                start_time=s_time,
                                delay=delay,
                                angular_speed=a_speed,
                                rand_center=rand_cnt
                            )
                        )
                    elif enemy.attack_data[i][0] == "wide_cone":
                        _, bul_num, cone_num, bul_data, angle, spd, d_angle, s_time, delay, a_speed = enemy.attack_data[i]
                        attack_data.extend(
                            AttackFunctions.wide_cone(
                                number_of_bullets=bul_num,
                                number_of_cones=cone_num,
                                bullet_data=BulletData(
                                    SpriteSheet(bul_data[0]).crop((bul_data[1], bul_data[2])),
                                    Collider(bul_data[3], bul_data[4])
                                ),
                                angle=angle,
                                speed=spd,
                                delta_angle=d_angle,
                                start_time=s_time,
                                delay=delay,
                                angular_speed=a_speed,
                                player=self._player,
                                enemy=enemy
                            )
                        )

                enemy.attack_data = sorted(attack_data, key=lambda x: x[1])

                self._enemies.append(enemy)
                self._enemy_count += 1

        for enemy in self._enemies:
            enemy.update()
            enemy.move()

        for bullet in self._player.bullets:
            on_screen = bullet.move(delta_time)
            if not on_screen:
                self._player.bullets.remove(bullet)
                del bullet

        for item in self._items:
            on_screen = item.move(delta_time, self._player)
            if not on_screen:
                self._items.remove(item)
                del item

        for effect in self._effects:
            ended = not effect.update(delta_time)
            if ended:
                self._effects.remove(effect)
                del effect

        if self._bullet_cleaner:
            self._bullet_cleaner.update(self._enemy_bullets, self, delta_time)
            if self._bullet_cleaner.kill:
                del self._bullet_cleaner
                self._bullet_cleaner = None

        for bullet in self._enemy_bullets:
            on_screen = bullet.move(delta_time)
            if not on_screen:
                self._enemy_bullets.remove(bullet)
                del bullet

        self._player.update()

    @render_fps
    def render(self, screen, clock):
        screen.fill((0, 0, 0), rect=self._game_zone)

        for bullet in self._player.bullets:
            self._bullet_group.add(bullet.get_sprite())

        for bullet in self._enemy_bullets:
            self._bullet_group.add(bullet.get_sprite())

        for item in self._items:
            self._item_group.add(item.get_sprite())

        for effect in self._effects:
            self._effect_group.add(effect.get_sprite())

        self._hud_group.add(self._bg)

        high_score = db_module.get_highscore()[0][0]

        if not high_score:
            high_score = 0

        hi_score_label = self._font.render(f"HiScore:    {format(high_score if high_score > self._player.points else self._player.points, '09d')}", True, (255, 255, 255)).convert_alpha()

        score_label = self._font.render(f"Score:    {format(self._player.points, '09d')}", True, (255, 255, 255)).convert_alpha()

        power_label = self._font.render(f"Power:    {format(round(self._player.power, 2), '.2f')} / 4.00", True,
                                       (255, 255, 255)).convert_alpha()

        hp_label = self._font.render(f"Player:   {'★' * self._player.hp}", True, (255, 255, 255)).convert_alpha()

        player_sprite = self._player.get_sprite()
        if self._player.slow or (self._player.reviving and self._player.invincibility_timer % 40 > 30):
            player_sprite.image.set_alpha(150)

        self._entity_group.add(player_sprite)

        for enemy in self._enemies:
            self._entity_group.add(enemy.get_sprite())

        self._entity_group.draw(screen)
        self._item_group.draw(screen)
        self._bullet_group.draw(screen)
        self._effect_group.draw(screen)

        if self._bullet_cleaner:
            screen.blit(self._bullet_cleaner.get_sprite(), (self._bullet_cleaner.collider.position - self._bullet_cleaner.collider.radius).to_tuple())

        if self._player.slow:
            player_hitbox_sprite = self._player.get_hitbox_sprite()
            screen.blit(player_hitbox_sprite, (self._player.position - (Vector2(*player_hitbox_sprite.get_size())) // 2).to_tuple())

        self._hud_group.draw(screen)

        screen.blit(hi_score_label, (self._game_zone[0] + self._game_zone[2] + 13, 160))
        screen.blit(score_label, (self._game_zone[0] + self._game_zone[2] + 50, 210))
        screen.blit(hp_label, (self._game_zone[0] + self._game_zone[2] + 50, 280))
        screen.blit(power_label, (self._game_zone[0] + self._game_zone[2] + 50, 330))

        self._effect_group.empty()
        self._entity_group.empty()
        self._item_group.empty()
        self._bullet_group.empty()
        self._bullet_group.empty()
        self._hud_group.empty()
