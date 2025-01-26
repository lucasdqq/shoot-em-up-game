import pygame.image
import time
from pygame.locals import *

from os.path import join as path_join

from SelectButtonMatrix import SelectButtonMatrix
from Vector2 import Vector2
from Ambiente import *
from Cenas import Scene, render_fps


class TitleScene(Scene):
    def __init__(self):
        super().__init__()

        self.background = pygame.sprite.Sprite()
        self.background.rect = (0, 0, WIDTH, HEIGHT)
        self.background.image = pygame.image.load(
            path_join("assets", "sprites", "backgrounds", "fumo.jpg")
        ).convert_alpha()

        self.font = pygame.font.Font(path_join("assets", "fonte.ttf"), 45)

        self.matrix = [[["Iniciar", self.switch_to_character]], [["Tabela de pontos", self.switch_to_scoreboard]], [["Sair", self.quit]]]
        self.ButtonMatrix = SelectButtonMatrix(Vector2(100, 100), self.matrix, self.font, (100, 100, 100), (255, 50, 40))

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

    def switch_to_character(self):
        from EscolherPersonagem import CharacterScene
        self.switch_to_scene(CharacterScene())

    def switch_to_scoreboard(self):
        from CenaRanking import ScoreboardScene
        self.switch_to_scene(ScoreboardScene())

    def quit(self):
        music_module.sounds[0](.1)
        time.sleep(.3)
        pygame.quit()

