import numpy
from pygame import Vector2


# chess piece
class Piece:
    def __init__(self, location: Vector2, piece_type: str, color: str):
        self.location: Vector2 = location
        self.type: str = piece_type
        self.color: str = color
        self.has_moved: bool = False

    # returns possible locations the node can go to at current position
    def possible_places(self) -> list[Vector2]:
        result: list[Vector2] = list()
        match self.type:
            case 'pawn':
                self.pawn_movement(result)

            case 'rook':
                self.rook_movement(result)

            case 'knight':
                self.knight_movement(result)

            case 'bishop':
                self.bishop_movement(result)

            case 'queen':
                self.queen_movement(result)

            case 'king':
                self.king_movement(result)

        return result

    def pawn_movement(self, result):
        if not self.has_moved:
            if self.color == 'white':
                result.append(Vector2(self.location.x, self.location.y + 2))
            else:
                result.append(Vector2(self.location.x, self.location.y - 2))
        if self.color == 'white':
            result.append(Vector2(self.location.x, self.location.y + 1))
        else:
            result.append(Vector2(self.location.x, self.location.y - 1))

    def rook_movement(self, result):
        # left side of rook
        if self.location.x > 1:
            for _ in range(1, self.location.x - 1):
                result.append(Vector2(self.location.x - _, self.location.y))
        # right side of rook
        if self.location.x < 8:
            for _ in range(self.location.x + 1, 9):
                result.append(Vector2(self.location.x + _, self.location.y))
        # top side of rook
        if self.location.y < 8:
            for _ in range(self.location.y + 1, 9):
                result.append(Vector2(self.location.x, self.location.y + _))
        # bottom side of rook
        if self.location.y > 1:
            for _ in range(1, self.location - 1):
                result.append(Vector2(self.location.x, self.location.y + _))

    def knight_movement(self, result):
        result.append(Vector2(self.location.x + 2, self.location.y + 1))  # right-right-up
        result.append(Vector2(self.location.x - 2, self.location.y + 1))  # left-left-up
        result.append(Vector2(self.location.x + 1, self.location.y + 2))  # up-up-right
        result.append(Vector2(self.location.x + 1, self.location.y - 2))  # down-down-up

    def bishop_movement(self, result):
        # top-right diagonal
        if self.location.x < 8 and self.location.y < 8:
            for _ in range(8 - numpy.maximum(self.location.x, self.location.y)):
                result.append(Vector2(self.location.x + _, self.location.y + _))
        # bottom-right diagonal
        if self.location.x < 8 and self.location.y > 1:
            for _ in range(numpy.minimum(8 - self.location.x, self.location.y - 1)):
                result.append(Vector2(self.location.x + _, self.location.y - _))
        # top-left diagonal
        if self.location.x > 1 and self.location.y < 8:
            for _ in range(numpy.minimum(self.location.x - 1, 8 - self.location.y)):
                result.append(Vector2(self.location.x - _, self.location.y + _))
        # bottom-left diagonal
        if self.location.x > 1 and self.location.y > 1:
            for _ in range(numpy.maximum(self.location.x, self.location.y) - 1):
                result.append(Vector2(self.location.x - _, self.location.y + _))

    def queen_movement(self, result):
        self.bishop_movement(result)
        self.rook_movement(result)

    def king_movement(self, result):
        #  top-right diagonal
        if self.location.x < 8 and self.location.y < 8:
            result.append(Vector2(self.location.x + 1, self.location.y + 1))
        # bottom-right diagonal
        if self.location.x < 8 and self.location.y > 1:
            result.append(Vector2(self.location.x + 1, self.location.y - 1))
        # top-left diagonal
        if self.location.x > 1 and self.location.y < 8:
            result.append(Vector2(self.location.x - 1, self.location.y + 1))
        # bottom-left diagonal
        if self.location.x > 1 and self.location.y > 1:
            result.append(Vector2(self.location.x - 1, self.location.y + 1))

        # left side of king
        if self.location.x > 1:
            result.append(Vector2(self.location.x - 1, self.location.y))
        # right side of king
        if self.location.x < 8:
            result.append(Vector2(self.location.x + 1, self.location.y))
        # top side of king
        if self.location.y < 8:
            result.append(Vector2(self.location.x, self.location.y + 1))
        # bottom side of king
        if self.location.y > 1:
            result.append(Vector2(self.location.x, self.location.y + 1))
