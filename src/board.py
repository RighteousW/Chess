import pygame.draw
from pygame import Rect, surface

from utils.constants import *
from utils.scripts import resize_image


class Board:
    def __init__(self, screen: surface):
        self.screen: surface = screen

        self.has_focus: bool = False  # if a valid piece has been clicked
        self.correct_player_focus: bool = False  # if focused piece is of the correct player
        self.focused_piece: Piece = DEFAULT_PIECE  # initialised as a non-valid piece

        # use every chess piece's location as an index to it in the dictionary
        self.chess_pieces: dict[(int, int):Piece] = dict()

        # determine who plays
        self.player_turn: str = 'white'

        self.initialize_pieces()

        self.grid_change: float = SCREEN_HEIGHT / 10

    # initial locations of chess_pieces
    def initialize_pieces(self):

        # initialize pawns
        for _ in range(1, 9):
            self.chess_pieces[_, 2] = Piece(Vector2(_, 2), 'pawn', 'white')
            self.chess_pieces[_, 7] = Piece(Vector2(_, 7), 'pawn', 'black')

        # initialize castles
        self.chess_pieces[1, 1] = Piece(Vector2(1, 1), 'rook', 'white')
        self.chess_pieces[8, 1] = Piece(Vector2(8, 1), 'rook', 'white')
        self.chess_pieces[1, 8] = Piece(Vector2(1, 8), 'rook', 'black')
        self.chess_pieces[8, 8] = Piece(Vector2(8, 8), 'rook', 'black')

        # initialize knight
        self.chess_pieces[2, 1] = Piece(Vector2(2, 1), 'knight', 'white')
        self.chess_pieces[7, 1] = Piece(Vector2(7, 1), 'knight', 'white')
        self.chess_pieces[2, 8] = Piece(Vector2(2, 8), 'knight', 'black')
        self.chess_pieces[7, 8] = Piece(Vector2(7, 8), 'knight', 'black')

        # initialize bishop
        self.chess_pieces[3, 1] = Piece(Vector2(3, 1), 'bishop', 'white')
        self.chess_pieces[6, 1] = Piece(Vector2(6, 1), 'bishop', 'white')
        self.chess_pieces[3, 8] = Piece(Vector2(3, 8), 'bishop', 'black')
        self.chess_pieces[6, 8] = Piece(Vector2(6, 8), 'bishop', 'black')

        # initialize queen
        self.chess_pieces[4, 1] = Piece(Vector2(4, 1), 'queen', 'white')
        self.chess_pieces[4, 8] = Piece(Vector2(4, 8), 'queen', 'black')

        # initialize king
        self.chess_pieces[5, 1] = Piece(Vector2(5, 1), 'king', 'white')
        self.chess_pieces[5, 8] = Piece(Vector2(5, 8), 'king', 'black')

    # draw the chess board
    def draw_board(self):
        for x in range(1, 9):
            for y in range(1, 9):
                if (x + y) % 2 != 0:
                    grid_color = COLOR_ULTRA_DARK_ORANGE
                else:
                    grid_color = COLOR_ULTRA_LIGHT_ORANGE
                pygame.draw.rect(self.screen, grid_color,
                                 Rect(x * self.grid_change, y * self.grid_change, self.grid_change, self.grid_change))

    # draw lines on borders that makes the board pop from background
    def draw_lines(self):
        # horizontal lines
        pygame.draw.line(self.screen, COLOR_WHITE,
                         (self.grid_change, self.grid_change),
                         (self.grid_change * 9, self.grid_change))
        pygame.draw.line(self.screen, COLOR_WHITE,
                         (self.grid_change, 9 * self.grid_change),
                         (self.grid_change * 9, 9 * self.grid_change))

        # vertical lines
        pygame.draw.line(self.screen, COLOR_WHITE,
                         (self.grid_change, self.grid_change),
                         (self.grid_change, self.grid_change * 9))
        pygame.draw.line(self.screen, COLOR_WHITE,
                         (9 * self.grid_change, self.grid_change),
                         (9 * self.grid_change, self.grid_change * 9))

    # draw images of chess chess_pieces
    def draw_chess_pieces(self):
        for chess_piece in self.chess_pieces.values():
            piece_image_file = CHESS_PIECE_IMAGES[f'{chess_piece.type}_{chess_piece.color}']
            piece_image = resize_image(piece_image_file, 40)

            self.screen.blit(piece_image, (chess_piece.location.x * self.grid_change + 10,
                                           chess_piece.location.y * self.grid_change + 10))

    def draw_focused_piece(self):
        if self.focused_piece != DEFAULT_PIECE:
            pygame.draw.rect(self.screen, COLOR_CYAN,
                             Rect(self.focused_piece.location.x * self.grid_change,
                                  self.focused_piece.location.y * self.grid_change,
                                  self.grid_change,
                                  self.grid_change))
            for location in self.focused_piece.possible_places():
                pass

    # renders the board, the borderlines and chess chess_pieces
    def render(self):
        self.draw_board()
        self.draw_lines()
        self.draw_focused_piece()
        self.draw_chess_pieces()

    # switch between player turns
    def switch_player(self):
        self.player_turn = 'black' if self.player_turn == 'white' else 'black'

    def right_press_at(self, location: tuple):
        x, y = location
        x = (x - (x % self.grid_change)) / self.grid_change
        y = (y - (y % self.grid_change)) / self.grid_change

        if self.chess_pieces[x, y]:
            self.has_focus = True
            self.focused_piece = self.chess_pieces[x, y]
