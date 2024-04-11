import sys

import pygame

from src.board import Board
from utils.constants import *


def keyboard_input():
    key_presses: [] = pygame.key.get_pressed()
    if key_presses[pygame.K_w]:
        pass


class Screen:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Chess')
        self.screen: pygame.surface = pygame.display.set_mode(SCREEN_DIMENSIONS)
        self.board: Board = Board(self.screen)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.can_left_click: bool = True

    def mouse_input(self):
        if self.can_left_click:
            left_click, middle_click, right_click = pygame.mouse.get_pressed(3)
            if left_click:
                self.board.left_press_at(pygame.mouse.get_pos())
                self.can_left_click = False
            if middle_click:
                pass
            if right_click:
                pass
        else:
            left_click, middle_click, right_click = pygame.mouse.get_pressed(3)
            if not left_click:
                self.can_left_click = True
            if middle_click:
                pass
            if right_click:
                pass

    def run(self):
        while True:
            self.screen.fill(COLOR_BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # exit on clicking X on window
                    pygame.quit()
                    sys.exit()

            # renders
            self.board.render()

            # inputs
            keyboard_input()
            self.mouse_input()

            pygame.display.flip()  # update screen
            self.clock.tick(FRAME_RATE)


Screen().run()
