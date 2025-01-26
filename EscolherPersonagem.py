import pygame.image
import time
from pygame.locals import *

from os.path import join as path_join

from SelectButtonMatrix import SelectButtonMatrix
from Vector2 import Vector2
from Ambiente import *
from Cenas import Scene, render_fps


class CharacterScene(Scene):
    def __init__(self):
        super().__init__()
        self.background = pygame.sprite.Sprite()
        self.background.rect = (0, 0, WIDTH, HEIGHT)
        self.background.image = pygame.image.load(
            path_join("assets", "sprites", "backgrounds", "cirno.jpg")
        ).convert_alpha()

        self.font = pygame.font.Font(path_join("assets", "fonte.ttf"), 45)
        self._selected_character = None
        self.matrix = [[["Jogar como Marisa", self.start_game_marisa]], [["Jogar como Reimu", self.start_game_reimu]], [["Voltar", self.switch_to_title]]]
        self.ButtonMatrix = SelectButtonMatrix(Vector2(100, 100), self.matrix, self.font, (100, 100, 100), (255, 50, 40))

    @property
    def selected_character(self):
        return self._selected_character

    @selected_character.setter
    def selected_character(self, value):
        if value in [0, 1]:
            self._selected_character = value
        else:
            raise ValueError("Character must be either 0 (Marisa) or 1 (Reimu)")

    @render_fps
    def render(self, screen, clock):
        background_group = pygame.sprite.RenderPlain()
        background_group.add(self.background)

        background_group.draw(screen)

        self.ButtonMatrix.draw(screen)

    def process_input(self, events):
        self.ButtonMatrix.handle_events(events)

        for evt in events:
            if evt.type == QUIT:
                pygame.quit()

    def start_game_marisa(self):
        from CenaJogo import GameScene
        self.selected_character = 0
        self.switch_to_scene(GameScene(self.selected_character))

    def start_game_reimu(self):
        from CenaJogo import GameScene
        self.selected_character = 1
        self.switch_to_scene(GameScene(self.selected_character))

    def switch_to_title(self):
        from CenaMenu import TitleScene
        self.switch_to_scene(TitleScene())
