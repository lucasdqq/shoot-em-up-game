from Colisao import Collider
from Sprites import SpriteSheet


class BulletData:
    def __init__(self, sprite_sheet: SpriteSheet, collider: Collider, animation_speed: int = 0):
        self._sprite_sheet = sprite_sheet
        self._collider = collider
        self._animation_speed = animation_speed

    @property
    def sprite_sheet(self):
        return self._sprite_sheet

    @sprite_sheet.setter
    def sprite_sheet(self, value):
        if isinstance(value, SpriteSheet):
            self._sprite_sheet = value
        else:
            raise ValueError("sprite_sheet must be an instance of SpriteSheet")

    @property
    def collider(self):
        return self._collider

    @collider.setter
    def collider(self, value):
        if isinstance(value, Collider):
            self._collider = value
        else:
            raise ValueError("collider must be an instance of Collider")

    @property
    def animation_speed(self):
        return self._animation_speed

    @animation_speed.setter
    def animation_speed(self, value):
        if isinstance(value, int) and value >= 0:
            self._animation_speed = value
        else:
            raise ValueError("animation_speed must be a non-negative integer")

    def __repr__(self):
        return f"BulletData({self.sprite_sheet}, {self.collider}, {self.animation_speed})"
