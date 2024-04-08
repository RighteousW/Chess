import sys

import pygame

from src.board import Board
from utils.constants import *

pygame.init()

pygame.display.set_caption('Chess')
screen: pygame.surface = pygame.display.set_mode(SCREEN_DIMENSIONS)
board: Board = Board(screen)
clock: pygame.time.Clock = pygame.time.Clock()


def keyboard_input():
    key_presses: [] = pygame.key.get_pressed()
    if key_presses[pygame.K_w]:
        pass


def mouse_input():
    left_click, middle_click, right_click = pygame.mouse.get_pressed(3)
    if left_click:
        board.right_press_at(pygame.mouse.get_pos())
    if middle_click:
        pass
    if right_click:
        pass


while True:
    screen.fill(COLOR_BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # exit on clicking X on window
            pygame.quit()
            sys.exit()

    # renders
    board.render()

    # inputs
    keyboard_input()
    mouse_input()

    pygame.display.flip()  # update screen
    clock.tick(FRAME_RATE)
