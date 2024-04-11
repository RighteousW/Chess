import pygame.draw
from pygame import Rect, surface

from utils.constants import *
from utils.scripts import resize_image


def in_bounds(x, y) -> bool:
    return 1 <= x <= 8 and 1 <= y <= 8


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

        self.grid_change: float = SCREEN_HEIGHT / 10  # distance between tiles in pixels

    # initial locations of chess_pieces
    def initialize_pieces(self):

        # initialize pawns
        for _ in range(1, 9):
            self.chess_pieces[_, 2] = Piece(Vector2(_, 2), 'pawn', 'black')
            self.chess_pieces[_, 7] = Piece(Vector2(_, 7), 'pawn', 'white')

        # initialize castles
        self.chess_pieces[1, 1] = Piece(Vector2(1, 1), 'rook', 'black')
        self.chess_pieces[8, 1] = Piece(Vector2(8, 1), 'rook', 'black')
        self.chess_pieces[1, 8] = Piece(Vector2(1, 8), 'rook', 'white')
        self.chess_pieces[8, 8] = Piece(Vector2(8, 8), 'rook', 'white')

        # initialize knight
        self.chess_pieces[2, 1] = Piece(Vector2(2, 1), 'knight', 'black')
        self.chess_pieces[7, 1] = Piece(Vector2(7, 1), 'knight', 'black')
        self.chess_pieces[2, 8] = Piece(Vector2(2, 8), 'knight', 'white')
        self.chess_pieces[7, 8] = Piece(Vector2(7, 8), 'knight', 'white')

        # initialize bishop
        self.chess_pieces[3, 1] = Piece(Vector2(3, 1), 'bishop', 'black')
        self.chess_pieces[6, 1] = Piece(Vector2(6, 1), 'bishop', 'black')
        self.chess_pieces[3, 8] = Piece(Vector2(3, 8), 'bishop', 'white')
        self.chess_pieces[6, 8] = Piece(Vector2(6, 8), 'bishop', 'white')

        # initialize queen
        self.chess_pieces[4, 1] = Piece(Vector2(4, 1), 'queen', 'black')
        self.chess_pieces[4, 8] = Piece(Vector2(4, 8), 'queen', 'white')

        # initialize king
        self.chess_pieces[5, 1] = Piece(Vector2(5, 1), 'king', 'black')
        self.chess_pieces[5, 8] = Piece(Vector2(5, 8), 'king', 'white')

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

    # draw lines on borders that makes the tiles more distinct
    def draw_lines(self):
        # horizontal lines
        for _ in range(1, 10):
            pygame.draw.line(self.screen, COLOR_WHITE,
                             (self.grid_change, _ * self.grid_change),
                             (self.grid_change * 9, _ * self.grid_change))

        # vertical lines
        for _ in range(1, 10):
            pygame.draw.line(self.screen, COLOR_WHITE,
                             (_ * self.grid_change, self.grid_change),
                             (_ * self.grid_change, self.grid_change * 9))

    # draw images of chess_pieces
    def draw_chess_pieces(self):
        for chess_piece in self.chess_pieces.values():
            piece_image_file = CHESS_PIECE_IMAGES[f'{chess_piece.type}_{chess_piece.color}']
            piece_image = resize_image(piece_image_file, 40)

            self.screen.blit(piece_image, (chess_piece.location.x * self.grid_change + 10,
                                           chess_piece.location.y * self.grid_change + 10))

    # changes tile color of focused tile to cyan and tiles it can move to as light cyan
    def draw_focused_piece(self):
        # check if selected tile is valid
        if self.focused_piece != DEFAULT_PIECE:

            # make color of selected tile cyan
            pygame.draw.rect(self.screen, COLOR_CYAN,
                             Rect(self.focused_piece.location.x * self.grid_change,
                                  self.focused_piece.location.y * self.grid_change,
                                  self.grid_change,
                                  self.grid_change))

            # dealing with pawn captures tile color
            if self.focused_piece.type == 'pawn':
                for x_coord, y_coord in self.focused_piece.pawn_capture():
                    if (x_coord, y_coord) in self.chess_pieces:
                        if self.chess_pieces[x_coord, y_coord].color != self.focused_piece.color:
                            pygame.draw.rect(self.screen, COLOR_LIGHT_CYAN,
                                             Rect(x_coord * self.grid_change,
                                                  y_coord * self.grid_change,
                                                  self.grid_change,
                                                  self.grid_change))

            # make color of possible tiles light cyan
            for (x, y) in self.focused_piece.possible_places():
                if (x, y) in self.chess_pieces.keys():
                    if self.chess_pieces[x, y].color != self.focused_piece.color:
                        pygame.draw.rect(self.screen, COLOR_LIGHT_CYAN,
                                         Rect(x * self.grid_change,
                                              y * self.grid_change,
                                              self.grid_change,
                                              self.grid_change))
                else:
                    pygame.draw.rect(self.screen, COLOR_LIGHT_CYAN,
                                     Rect(x * self.grid_change,
                                          y * self.grid_change,
                                          self.grid_change,
                                          self.grid_change))

    # renders the board, the borderlines and chess chess_pieces
    def render(self):
        self.draw_board()
        self.draw_focused_piece()
        self.draw_lines()
        self.draw_chess_pieces()

    # switch between player turns
    def switch_player(self):
        self.player_turn = 'black' if self.player_turn == 'white' else 'white'

    # on the event of left click on screen
    def left_press_at(self, location: tuple):
        x, y = location

        # convert clicked pixel coordinates to tile coordinates
        x = (x - (x % self.grid_change)) / self.grid_change
        y = (y - (y % self.grid_change)) / self.grid_change

        # dealing with pawn captures
        pawn_can_capture: list[tuple] = list()
        if self.focused_piece.type == 'pawn':
            for x_coord, y_coord in self.focused_piece.pawn_capture():
                if (x_coord, y_coord) in self.chess_pieces:
                    if self.chess_pieces[x_coord, y_coord].color != self.focused_piece.color:
                        pawn_can_capture.append((x_coord, y_coord))

        # if a piece is already selected try to move it to clicked tile
        if self.has_focus and self.focused_piece.color == self.player_turn and in_bounds(x, y):
            if (x, y) in self.focused_piece.possible_places() or (x, y) in pawn_can_capture:
                is_empty_space = (x, y) not in self.chess_pieces

                # only move if destination tile is an enemy piece or an empty tile
                if is_empty_space or (not is_empty_space and self.chess_pieces[x, y].color != self.focused_piece.color):
                    self.has_focus = False
                    self.chess_pieces[x, y] = Piece(Vector2(x, y), self.focused_piece.type, self.focused_piece.color)
                    self.chess_pieces.pop((self.focused_piece.location.x, self.focused_piece.location.y))
                    self.focused_piece = DEFAULT_PIECE
                    self.chess_pieces[x, y].has_moved = True
                    self.switch_player()

        # if no piece is selected, selected piece at clicked tile
        elif (x, y) in self.chess_pieces:
            self.has_focus = True
            self.focused_piece = self.chess_pieces[x, y]
