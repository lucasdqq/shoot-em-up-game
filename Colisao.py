from __future__ import annotations

from Vector2 import Vector2


class Collider:
    def __init__(self, radius: float, position: Vector2 = Vector2.zero(), offset: Vector2 = Vector2.zero()):
        self._radius = radius
        self._position = position
        self._offset = offset

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float):
        if value > 0:
            self._radius = value
        else:
            raise ValueError("Radius must be positive")

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, value: Vector2):
        self._position = value

    @property
    def offset(self) -> Vector2:
        return self._offset

    @offset.setter
    def offset(self, value: Vector2):
        self._offset = value

    def check_collision(self, target: Collider) -> bool:
        return ((target.position - self.position) * (target.position - self.position)).length() < (self.radius + target.radius) ** 2

    def __repr__(self):
        return f"Collider({self.radius}, {self.position}, {self.offset})"
