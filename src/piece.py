import pygame


# chess piece
class Piece:
    def __init__(self):
        self.location: pygame.Vector2
        self.type: str
