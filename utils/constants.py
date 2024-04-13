from pygame.color import THECOLORS, Color

from pygame import Vector2
from src.piece import Piece

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)

FRAME_RATE = 120

COLOR_BLACK = THECOLORS['black']
COLOR_WHITE = THECOLORS['white']
COLOR_CYAN = THECOLORS['cyan']
COLOR_LIGHT_CYAN = THECOLORS['lightcyan']
LIGHT_TILE_COLOR = Color(254, 231, 201)
DARK_TILE_COLOR = Color(64, 36, 40)

POSSIBLE_PROMOTIONS = {
    'pawn',
    'rook',
    'knight',
    'bishop',
    'queen'
}

CHESS_PIECE_IMAGES = {
    'pawn_black': 'data/chess_pieces/png/pawn_black.png',
    'pawn_white': 'data/chess_pieces/png/pawn_white.png',
    'pawn_blue': 'data/chess_pieces/png/pawn_blue.png',

    'rook_black': 'data/chess_pieces/png/rook_black.png',
    'rook_white': 'data/chess_pieces/png/rook_white.png',
    'rook_blue': 'data/chess_pieces/png/rook_blue.png',

    'knight_black': 'data/chess_pieces/png/knight_black.png',
    'knight_white': 'data/chess_pieces/png/knight_white.png',
    'knight_blue': 'data/chess_pieces/png/knight_blue.png',

    'bishop_black': 'data/chess_pieces/png/bishop_black.png',
    'bishop_white': 'data/chess_pieces/png/bishop_white.png',
    'bishop_blue': 'data/chess_pieces/png/bishop_blue.png',

    'queen_black': 'data/chess_pieces/png/queen_black.png',
    'queen_white': 'data/chess_pieces/png/queen_white.png',
    'queen_blue': 'data/chess_pieces/png/queen_blue.png',

    'king_black': 'data/chess_pieces/png/king_black.png',
    'king_white': 'data/chess_pieces/png/king_white.png',
    'king_blue': 'data/chess_pieces/png/king_blue.png',
}

# making piece out of screen bounds hence when comparing pieces will always be -ve
DEFAULT_PIECE: Piece = Piece(Vector2(1000, 1000), 'pawn', 'black')
