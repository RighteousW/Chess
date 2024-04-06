import sys

import pygame

from src.board import Board
from utils.constants import *

pygame.init()

pygame.display.set_caption('Chess')
screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
board = Board(screen)
clock = pygame.time.Clock()


def keyboard_input():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        pass


while True:
    screen.fill(COLOR_BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # renders
    board.render()

    # inputs
    keyboard_input()

    pygame.display.flip()
    clock.tick(FRAME_RATE)
