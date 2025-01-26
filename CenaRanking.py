import pygame
import datetime
from pygame.locals import *
from os.path import join as path_join

from Player import Player
from Cenas import Scene, render_fps
from Rankings import ScoreboardLine
from SelectButtonMatrix import SelectButtonMatrix
from Vector2 import Vector2
from Ambiente import WIDTH, HEIGHT, db_module, music_module
from Funcoes import clamp

class ScoreboardScene(Scene):
    def __init__(self, player: Player = None):
        super().__init__()

        music_module.stop_music()

        self.MAX_NAME_LENGTH = 8

        self.font = pygame.font.Font(path_join("assets", "fonte.ttf"), 24)
        self.player = player

        self.leaderboard = list(map(lambda x: ScoreboardLine(*x), db_module.get_leaderboard()))
        self.leaderboard.sort(reverse=True)

        if player is not None:
            self.cursor = 0
            self.statistics = ScoreboardLine(
                " " * self.MAX_NAME_LENGTH,
                self.player.points,
                datetime.date.today().strftime("%d/%m/%y"),
                round(self.player.slowRate.tan(), 2),
                True
            )

            if len(self.leaderboard) < 10 or self.statistics > self.leaderboard[-1]:
                self.leaderboard.append(self.statistics)
                self.leaderboard.sort(reverse=True)
                if len(self.leaderboard) > 10:
                    self.leaderboard.pop(-1)
            else:
                self.switch_to_menu()

            self._name = " " * self.MAX_NAME_LENGTH

            self.matrix = [
                [[char, lambda char=char: self.type_letter(char)] for char in "ABCDEFGHIJKLMNOP"],
                [[char, lambda char=char: self.type_letter(char)] for char in "QRSTUVWXYZ.,:;_@"],
                [[char, lambda char=char: self.type_letter(char)] for char in "abcdefghijklmnop"],
                [[char, lambda char=char: self.type_letter(char)] for char in "qrstuvwxyz+-/*=%"],
                [[char, lambda char=char: self.type_letter(char)] for char in "0123456789#!?\'\"$"],
                [[char, lambda char=char: self.type_letter(char)] for char in "(){}[]<>&|~^  "] + [["←", self.delete_letter]] + [["End", self.save]]
            ]
            self.keyboard = SelectButtonMatrix(
                Vector2(WIDTH // 2 - 250, HEIGHT // 2 + 150),
                self.matrix,
                self.font,
                (100, 100, 100),
                (255, 50, 40),
                padding=Vector2(30, 35)
            )
            self.keyboard.cursor = Vector2(15, 5)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value.ljust(self.MAX_NAME_LENGTH)

    def type_letter(self, char: str):
        if self.cursor >= self.MAX_NAME_LENGTH:
            self.save()
            return
        name_list = list(self._name)
        name_list[self.cursor] = char
        self._name = ''.join(name_list)
        self.cursor += 1

    def delete_letter(self):
        name_list = list(self._name)

        if self.cursor == self.MAX_NAME_LENGTH:
            self.cursor -= 1

        if self._name[self.cursor] != " ":
            name_list[self.cursor] = " "
        else:
            self.cursor = clamp(self.cursor - 1, 0, self.MAX_NAME_LENGTH - 1)
            name_list[self.cursor] = " "

        self._name = "{:8}".format(''.join(name_list))

    def process_input(self, events):
        if self.player is not None:
            self.keyboard.handle_events(events)

        for evt in events:
            if evt.type == QUIT:
                pygame.quit()
            if evt.type == pygame.KEYDOWN:
                if evt.key == K_x:
                    music_module.sounds[0](.1)
                    if self.player is not None:
                        self.delete_letter()
                    else:
                        self.switch_to_menu()

    def text_render(self, screen, text: str, position: Vector2, padding: int, color=(255, 255, 255)):
        for i in range(len(text)):
            letter = text[i]
            letter_label = self.font.render(letter, True, color).convert_alpha()
            screen.blit(letter_label, (position + Vector2(padding, 0) * i).to_tuple())

    @render_fps
    def render(self, screen, clock):
        screen.fill((0, 0, 0))

        self.text_render(screen, "No   Name            Score       Date      Slow", Vector2(100, 60), 20)

        for i in range(len(self.leaderboard)):
            line = self.leaderboard[i]
            if not line.player:
                self.text_render(screen, "{:2}   ".format(i + 1) + str(line), Vector2(100, 100 + i * 30), 20, (255, 150, 150))
            else:
                self.text_render(screen, "     " + " " * clamp(self.cursor, 0, self.MAX_NAME_LENGTH - 1) + "_" + " " * (self.MAX_NAME_LENGTH - clamp(self.cursor, 0, self.MAX_NAME_LENGTH - 1) - 1),  Vector2(100, 100 + i * 30), 20)
                self.text_render(screen, "{:2}   ".format(i + 1) + (self._name if self._name != " " * self.MAX_NAME_LENGTH else "_" * self.MAX_NAME_LENGTH) + str(line)[8:],  Vector2(100, 100 + i * 30), 20)

        if self.player is not None:
            self.keyboard.draw(screen)

    def switch_to_menu(self):
        from CenaMenu import TitleScene
        self.switch_to_scene(TitleScene())

    def save(self):
        self.statistics.name = self._name
        if self.statistics.name != " " * self.MAX_NAME_LENGTH:
            db_module.add_to_leaderboard(self.statistics)
        self.switch_to_menu()
