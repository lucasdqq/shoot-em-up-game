import pygame
from typing import Union

from Sprites import SpriteSheet
from Vector2 import Vector2


class Entity:
    def __init__(self):
        self._position = Vector2()
        self._sprite_sheet: Union[SpriteSheet, list[pygame.sprite.Sprite]] = []
        self._name: str = ""

        self.current_sprite = 0
        self.change_sprite_timer = 0

        self.sprite = pygame.sprite.Sprite()

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, value: Vector2) -> None:
        self._position = value

    @property
    def sprite_sheet(self) -> Union[SpriteSheet, list[pygame.sprite.Sprite]]:
        return self._sprite_sheet

    @sprite_sheet.setter
    def sprite_sheet(self, value: Union[SpriteSheet, list[pygame.sprite.Sprite]]) -> None:
        self._sprite_sheet = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    def update(self) -> None:
        pass

    def next_sprite(self, delay: int) -> None:
        if self.change_sprite_timer >= delay:
            self.current_sprite = (self.current_sprite + 1) % len(self.sprite_sheet)
            self.change_sprite_timer = 0

    def get_sprite(self) -> pygame.sprite.Sprite:
        self.sprite.image = self.sprite_sheet[self.current_sprite]

        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.center = self.position.to_tuple()

        return self.sprite
