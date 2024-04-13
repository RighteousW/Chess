from pygame import Vector2


# chess piece
class Piece:
    def __init__(self, location: Vector2, piece_type: str, color: str):
        self.location: Vector2 = location
        self.type: str = piece_type
        self.color: str = color
        self.has_moved: bool = False
