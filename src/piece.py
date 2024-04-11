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
    def possible_places(self) -> list[tuple]:
        result: list[tuple] = list()
        x = int(self.location.x)
        y = int(self.location.y)

        match self.type:
            case 'pawn':
                self.pawn_movement(result)

            case 'rook':
                self.rook_movement(result, x, y)

            case 'knight':
                self.knight_movement(result, x, y)

            case 'bishop':
                self.bishop_movement(result, x, y)

            case 'queen':
                self.queen_movement(result, x, y)

            case 'king':
                self.king_movement(result, x, y)

        return result

    def pawn_capture(self):
        result: list[(float, float)] = list()
        if self.color == 'black':
            if self.location.x > 1:
                result.append((self.location.x - 1, self.location.y + 1))
            if self.location.x < 8:
                result.append((self.location.x + 1, self.location.y + 1))
        elif self.color == 'white':
            if self.location.x > 1:
                result.append((self.location.x - 1, self.location.y - 1))
            if self.location.x < 8:
                result.append((self.location.x + 1, self.location.y - 1))
        return result

    def pawn_movement(self, result):
        if not self.has_moved:
            if self.color == 'black':
                result.append((self.location.x, self.location.y + 2))
            else:
                result.append((self.location.x, self.location.y - 2))
        if self.color == 'black':
            result.append((self.location.x, self.location.y + 1))
        elif self.color == 'white':
            result.append((self.location.x, self.location.y - 1))

    def rook_movement(self, result, x, y):
        # left side of rook
        if x > 1:
            for _ in range(1, x):
                result.append((self.location.x - _, self.location.y))
        # right side of rook
        if x < 8:
            for _ in range(1, 9 - x):
                result.append((self.location.x + _, self.location.y))
        # top side of rook
        if y > 1:
            for _ in range(1, y):
                result.append((self.location.x, self.location.y - _))
        # bottom side of rook
        if y < 8:
            for _ in range(1, 9 - y):
                result.append((self.location.x, self.location.y + _))

    def knight_movement(self, result, x, y):
        if x < 7 and y > 1:
            result.append((self.location.x + 2, self.location.y - 1))  # right-right-up

        if x < 7 and y < 8:
            result.append((self.location.x + 2, self.location.y + 1))  # right-right-down

        if x > 2 and y > 1:
            result.append((self.location.x - 2, self.location.y - 1))  # left-left-up

        if x > 2 and y < 8:
            result.append((self.location.x - 2, self.location.y + 1))  # left-left-down

        if x < 8 and y > 2:
            result.append((self.location.x + 1, self.location.y - 2))  # up-up-right

        if x > 1 and y > 2:
            result.append((self.location.x - 1, self.location.y - 2))  # up-up-left

        if x < 8 and y < 7:
            result.append((self.location.x + 1, self.location.y + 2))  # down-down-right

        if x > 1 and y < 7:
            result.append((self.location.x - 1, self.location.y + 2))  # down-down-left

    def bishop_movement(self, result, x, y):
        # top-right diagonal
        if x < 8 and y > 1:
            for _ in range(10 - numpy.minimum(x, y)):
                result.append((self.location.x + _, self.location.y - _))
        # bottom-right diagonal
        if x < 8 and y < 8:
            for _ in range(numpy.maximum(9 - x, y - 1)):
                result.append((self.location.x + _, self.location.y + _))
        # top-left diagonal
        if x > 1 and y > 1:
            for _ in range(numpy.minimum(x - 1, y - 1) + 1):
                result.append((self.location.x - _, self.location.y - _))
        # bottom-left diagonal
        if x > 1 and y < 8:
            for _ in range(numpy.maximum(x, y)):
                result.append((self.location.x - _, self.location.y + _))

    def queen_movement(self, result, x, y):
        self.bishop_movement(result, x, y)
        self.rook_movement(result, x, y)

    def king_movement(self, result, x, y):
        #  top-right diagonal
        if x < 8 and y > 1:
            result.append((self.location.x + 1, self.location.y - 1))
        # bottom-right diagonal
        if x < 8 and y < 8:
            result.append((self.location.x + 1, self.location.y + 1))
        # top-left diagonal
        if x > 1 and y > 1:
            result.append((self.location.x - 1, self.location.y - 1))
        # bottom-left diagonal
        if x > 1 and y < 8:
            result.append((self.location.x - 1, self.location.y + 1))

        # left side of king
        if x > 1:
            result.append((self.location.x - 1, self.location.y))
        # right side of king
        if x < 8:
            result.append(Vector2(self.location.x + 1, self.location.y))
        # top side of king
        if y > 1:
            result.append((self.location.x, self.location.y - 1))
        # bottom side of king
        if y < 8:
            result.append((self.location.x, self.location.y + 1))
