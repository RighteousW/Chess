from pygame import Vector2
from pygame.color import Color

from src.piece import Piece

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)

FRAME_RATE = 120

COLOR_BLACK = Color(0, 0, 0)
COLOR_WHITE = Color(255, 255, 255)
COLOR_SELECTED_PIECE = Color(0, 200, 200)
COLOR_POSSIBLE_TILES = Color(0, 240, 140)
LIGHT_TILE_COLOR = Color(242, 225, 195)
DARK_TILE_COLOR = Color(195, 160, 130)

POSSIBLE_PROMOTIONS = {
    'pawn',
    'rook',
    'knight',
    'bishop',
    'queen'
}
PIECE_VALUES = {
    'pawn': 1,
    'rook': 5,
    'knight': 3,
    'bishop': 3,
    'queen': 9,
    'king': 30
}

CHESS_PIECE_IMAGES = {
    'pawn_black': 'data/chess_pieces/pawn_black.png',
    'pawn_white': 'data/chess_pieces/pawn_white.png',

    'rook_black': 'data/chess_pieces/rook_black.png',
    'rook_white': 'data/chess_pieces/rook_white.png',

    'knight_black': 'data/chess_pieces/knight_black.png',
    'knight_white': 'data/chess_pieces/knight_white.png',

    'bishop_black': 'data/chess_pieces/bishop_black.png',
    'bishop_white': 'data/chess_pieces/bishop_white.png',

    'queen_black': 'data/chess_pieces/queen_black.png',
    'queen_white': 'data/chess_pieces/queen_white.png',

    'king_black': 'data/chess_pieces/king_black.png',
    'king_white': 'data/chess_pieces/king_white.png',
}

# making king out of screen bounds hence when comparing pieces will always be -ve
DEFAULT_PIECE: Piece = Piece(Vector2(1000, 1000), 'pawn', 'black')
