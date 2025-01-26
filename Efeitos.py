import pygame
from Vector2 import Vector2

class Effect:
    def __init__(self, position: Vector2, sprite_sheet: [pygame.Surface, ...], delay: float):
        self._position = position
        self._sprite_sheet = sprite_sheet
        self._current_sprite = 0
        self._sprite_timer = 0
        self._delay = delay

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, value: Vector2):
        self._position = value

    @property
    def sprite_sheet(self):
        return self._sprite_sheet

    @property
    def delay(self) -> float:
        return self._delay

    def update(self, delta_time) -> bool:
        self._sprite_timer += delta_time * 60 * 2
        if self._sprite_timer >= self._delay:
            self._current_sprite += 1
            self._sprite_timer = 0

            if self._current_sprite >= len(self._sprite_sheet):
                return False

        return True

    def get_sprite(self) -> pygame.sprite.Sprite:
        sprite = pygame.sprite.Sprite()
        sprite.image = self._sprite_sheet[self._current_sprite]
        sprite.rect = sprite.image.get_rect()
        sprite.rect.center = self._position.to_tuple()
        return sprite
