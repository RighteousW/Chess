from pygame import surface

from src.piece import Piece, Vector2


class Board:
    def __init__(self, screen: surface):
        self.screen: surface = screen

        # use every chess piece's location as an index to it in the dictionary
        self.pieces: dict[(int, int):Piece] = dict()

        # determine who plays
        self.player_turn: int = 1

        self.initialize_pieces()

    # initial locations of pieces
    def initialize_pieces(self):

        # initialize pawns
        for _ in range(1, 9):
            self.pieces[2, _] = Piece(Vector2(1, _), 'pawn', 'white')
            self.pieces[7, _] = Piece(Vector2(6, _), 'pawn', 'black')

        # initialize castles
        self.pieces[1, 1] = Piece(Vector2(1, 1), 'rook', 'white')
        self.pieces[1, 8] = Piece(Vector2(1, 8), 'rook', 'white')
        self.pieces[8, 1] = Piece(Vector2(8, 1), 'rook', 'black')
        self.pieces[8, 8] = Piece(Vector2(8, 8), 'rook', 'black')

        # initialize knight
        self.pieces[1, 2] = Piece(Vector2(1, 2), 'knight', 'white')
        self.pieces[1, 7] = Piece(Vector2(1, 7), 'knight', 'white')
        self.pieces[8, 2] = Piece(Vector2(8, 2), 'knight', 'black')
        self.pieces[8, 7] = Piece(Vector2(8, 7), 'knight', 'black')

        # initialize bishop
        self.pieces[1, 3] = Piece(Vector2(1, 3), 'bishop', 'white')
        self.pieces[1, 6] = Piece(Vector2(1, 6), 'bishop', 'white')
        self.pieces[8, 3] = Piece(Vector2(8, 3), 'bishop', 'black')
        self.pieces[8, 6] = Piece(Vector2(8, 7), 'bishop', 'black')

        # initialize queen
        self.pieces[1, 4] = Piece(Vector2(1, 4), 'queen', 'white')
        self.pieces[8, 4] = Piece(Vector2(8, 4), 'queen', 'black')

        # initialize king
        self.pieces[1, 5] = Piece(Vector2(1, 5), 'king', 'white')
        self.pieces[8, 5] = Piece(Vector2(8, 5), 'king', 'black')

    # switch between player turns
    def switch_player(self):
        self.player_turn *= -1
