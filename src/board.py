import numpy as np

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

        # piece to test movement
        # self.chess_pieces[4.0, 4.0] = Piece(Vector2(4.0, 4.0), 'bishop', 'white')

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
                    grid_color = DARK_TILE_COLOR
                else:
                    grid_color = LIGHT_TILE_COLOR
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

            # make color of possible tiles light cyan
            for (x, y) in self.possible_places(self.focused_piece):
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
        self.draw_chess_pieces()
        self.draw_lines()

    # switch between player turns
    def switch_player(self):
        self.player_turn = 'black' if self.player_turn == 'white' else 'white'

    # on the event of left click on screen
    def left_press_at(self, location: tuple):
        x, y = location

        # convert clicked pixel coordinates to tile coordinates
        x = (x - (x % self.grid_change)) / self.grid_change
        y = (y - (y % self.grid_change)) / self.grid_change

        # if a piece is already selected try to move it to the clicked tile
        if self.has_focus and self.focused_piece.color == self.player_turn and in_bounds(x, y):
            if (x, y) in self.possible_places(self.focused_piece):
                is_empty_space = (x, y) not in self.chess_pieces

                # only move if destination tile is an enemy piece or an empty tile
                if is_empty_space or (not is_empty_space and self.chess_pieces[x, y].color != self.focused_piece.color):
                    self.has_focus = False
                    self.chess_pieces[x, y] = Piece(Vector2(x, y), self.focused_piece.type, self.focused_piece.color)
                    self.chess_pieces.pop((self.focused_piece.location.x, self.focused_piece.location.y))
                    self.focused_piece = DEFAULT_PIECE
                    self.chess_pieces[x, y].has_moved = True
                    self.switch_player()

                else:
                    self.has_focus = True
                    self.focused_piece = self.chess_pieces[x, y]
            else:
                self.has_focus = True
                self.focused_piece = self.chess_pieces[x, y]

        # if no piece is selected, select piece at clicked tile
        elif (x, y) in self.chess_pieces:
            self.has_focus = True
            self.focused_piece = self.chess_pieces[x, y]

    # returns possible locations the piece can go to at current position
    def possible_places(self, piece: Piece) -> list[tuple]:
        result: list[tuple] = list()

        match piece.type:
            case 'pawn':
                self.pawn_movement(result, piece)
                self.pawn_capture(result, piece)

            case 'rook':
                self.rook_movement(result, piece)

            case 'knight':
                self.knight_movement(result, piece)

            case 'bishop':
                self.bishop_movement(result, piece)

            case 'queen':
                self.queen_movement(result, piece)

            case 'king':
                self.king_movement(result, piece)

        return result

    def pawn_capture(self, result, pawn_piece: Piece):
        right_black = (pawn_piece.location.x - 1, pawn_piece.location.y + 1)
        right_white = (pawn_piece.location.x + 1, pawn_piece.location.y - 1)
        left_black = (pawn_piece.location.x + 1, pawn_piece.location.y + 1)
        left_white = (pawn_piece.location.x - 1, pawn_piece.location.y - 1)

        if pawn_piece.color == 'black':
            if pawn_piece.location.x > 1 and right_black in self.chess_pieces.keys():
                if self.chess_pieces[right_black].color != pawn_piece.color:
                    result.append(right_black)

            if pawn_piece.location.x < 8 and left_black in self.chess_pieces.keys():
                if self.chess_pieces[left_black].color != pawn_piece.color:
                    result.append(left_black)

        elif pawn_piece.color == 'white':
            if pawn_piece.location.x > 1 and left_white in self.chess_pieces.keys():
                if self.chess_pieces[left_white].color != pawn_piece.color:
                    result.append(left_white)

            if pawn_piece.location.x < 8 and right_white in self.chess_pieces.keys():
                if self.chess_pieces[right_white].color != pawn_piece.color:
                    result.append(right_white)

        return result

    def pawn_movement(self, result, piece):
        one_white = (piece.location.x, piece.location.y - 1)  # 1 tile in front of piece
        one_black = (piece.location.x, piece.location.y + 1)
        two_white = (piece.location.x, piece.location.y - 2)  # 2 tiles in front of piece
        two_black = (piece.location.x, piece.location.y + 2)

        # first pawn movement, able to move two spaces
        if not piece.has_moved:
            if (piece.color == 'black' and
                    two_black not in self.chess_pieces.keys() and
                    one_black not in self.chess_pieces.keys()):
                result.append(two_black)
            elif (piece.color == 'white' and
                  two_white not in self.chess_pieces.keys() and
                  one_white not in self.chess_pieces.keys()):
                result.append(two_white)

        # normal pawn movement
        if piece.color == 'black' and one_black not in self.chess_pieces.keys():
            result.append(one_black)
        elif piece.color == 'white' and one_white not in self.chess_pieces.keys():
            result.append(one_white)

    def rook_movement(self, result, piece: Piece):
        x = int(piece.location.x)
        y = int(piece.location.y)

        top_collided: bool = False
        bottom_collided: bool = False
        right_collided: bool = False
        left_collided: bool = False

        # left side of rook
        if x > 1:
            for _ in range(1, x):
                if not left_collided:
                    result.append((piece.location.x - _, piece.location.y))
                    if (piece.location.x - _, piece.location.y) in self.chess_pieces.keys():
                        break
        # right side of rook
        if x < 8:
            for _ in range(1, 9 - x):
                if not right_collided:
                    result.append((piece.location.x + _, piece.location.y))
                    if (piece.location.x + _, piece.location.y) in self.chess_pieces.keys():
                        break
        # top side of rook
        if y > 1:
            for _ in range(1, y):
                if not top_collided:
                    result.append((piece.location.x, piece.location.y - _))
                    if (piece.location.x, piece.location.y - _) in self.chess_pieces.keys():
                        break
        # bottom side of rook
        if y < 8:
            for _ in range(1, 9 - y):
                if not bottom_collided:
                    result.append((piece.location.x, piece.location.y + _))
                    if (piece.location.x, piece.location.y + _) in self.chess_pieces.keys():
                        break

    def knight_movement(self, result, piece: Piece):
        x = int(piece.location.x)
        y = int(piece.location.y)

        if x < 7 and y > 1:  # right-right-up
            if (piece.location.x + 2, piece.location.y - 1) not in self.chess_pieces.keys():
                result.append((piece.location.x + 2, piece.location.y - 1))
            elif self.chess_pieces[(piece.location.x + 2, piece.location.y - 1)].color != piece.color:
                result.append((piece.location.x + 2, piece.location.y - 1))

        if x < 7 and y < 8:  # right-right-down
            if (piece.location.x + 2, piece.location.y + 1) not in self.chess_pieces.keys():
                result.append((piece.location.x + 2, piece.location.y + 1))
            elif self.chess_pieces[(piece.location.x + 2, piece.location.y + 1)].color != piece.color:
                result.append((piece.location.x + 2, piece.location.y + 1))

        if x > 2 and y > 1:  # left-left-up
            if (piece.location.x - 2, piece.location.y - 1) not in self.chess_pieces.keys():
                result.append((piece.location.x - 2, piece.location.y - 1))
            elif self.chess_pieces[(piece.location.x - 2, piece.location.y - 1)].color != piece.color:
                result.append((piece.location.x - 2, piece.location.y - 1))

        if x > 2 and y < 8:  # left-left-down
            if (piece.location.x - 2, piece.location.y + 1) not in self.chess_pieces.keys():
                result.append((piece.location.x - 2, piece.location.y + 1))
            elif self.chess_pieces[(piece.location.x - 2, piece.location.y + 1)].color != piece.color:
                result.append((piece.location.x - 2, piece.location.y + 1))

        if x < 8 and y > 2:  # up-up-right
            if (piece.location.x + 1, piece.location.y - 2) not in self.chess_pieces.keys():
                result.append((piece.location.x + 1, piece.location.y - 2))
            elif self.chess_pieces[(piece.location.x + 1, piece.location.y - 2)].color != piece.color:
                result.append((piece.location.x + 1, piece.location.y - 2))

        if x > 1 and y > 2:  # up-up-left
            result.append((piece.location.x - 1, piece.location.y - 2))
            if (piece.location.x - 1, piece.location.y - 2) not in self.chess_pieces.keys():
                result.append((piece.location.x - 1, piece.location.y - 2))
            elif self.chess_pieces[(piece.location.x - 1, piece.location.y - 2)].color != piece.color:
                result.append((piece.location.x - 1, piece.location.y - 2))

        if x < 8 and y < 7:  # down-down-right
            if (piece.location.x + 1, piece.location.y + 2) not in self.chess_pieces.keys():
                result.append((piece.location.x + 1, piece.location.y + 2))
            elif self.chess_pieces[(piece.location.x + 1, piece.location.y + 2)].color != piece.color:
                result.append((piece.location.x + 1, piece.location.y + 2))

        if x > 1 and y < 7:  # down-down-left
            if (piece.location.x - 1, piece.location.y + 2) not in self.chess_pieces.keys():
                result.append((piece.location.x - 1, piece.location.y + 2))
            elif self.chess_pieces[(piece.location.x - 1, piece.location.y + 2)].color != piece.color:
                result.append((piece.location.x - 1, piece.location.y + 2))

    def bishop_movement(self, result, piece: Piece):
        x = int(piece.location.x)
        y = int(piece.location.y)

        # top-right diagonal
        if x < 8 and y > 1:
            for _ in range(1, 8 - np.maximum(x, y)):
                if (piece.location.x + _, piece.location.y - _) in self.chess_pieces.keys():
                    result.append((piece.location.x + _, piece.location.y - _))
                    break
                result.append((piece.location.x + _, piece.location.y - _))

        # bottom-right diagonal
        if x < 8 and y < 8:
            for _ in range(1, np.maximum(9 - x, y - 1)):
                if (piece.location.x + _, piece.location.y + _) in self.chess_pieces.keys():
                    result.append((piece.location.x + _, piece.location.y + _))
                    break
                result.append((piece.location.x + _, piece.location.y + _))

        # top-left diagonal
        if x > 1 and y > 1:
            for _ in range(1, np.minimum(x - 1, y - 1) + 1):
                if (piece.location.x - _, piece.location.y - _) in self.chess_pieces.keys():
                    result.append((piece.location.x - _, piece.location.y - _))
                    break
                result.append((piece.location.x - _, piece.location.y - _))

        # bottom-left diagonal
        if x > 1 and y < 8:
            for _ in range(1, np.maximum(x, y)):
                if (piece.location.x - _, piece.location.y + _) in self.chess_pieces.keys():
                    result.append((piece.location.x - _, piece.location.y + _))
                    break
                result.append((piece.location.x - _, piece.location.y + _))

    def queen_movement(self, result, piece: Piece):
        self.bishop_movement(result, piece)
        self.rook_movement(result, piece)

    def king_movement(self, result, piece: Piece):
        x = int(piece.location.x)
        y = int(piece.location.y)

        top_right = (piece.location.x + 1, piece.location.y - 1)
        top_left = (piece.location.x - 1, piece.location.y - 1)
        bottom_left = (piece.location.x - 1, piece.location.y + 1)
        bottom_right = (piece.location.x + 1, piece.location.y + 1)

        #  top-right diagonal
        if x < 8 and y > 1:
            if top_right not in self.chess_pieces.keys():
                result.append(top_right)
            elif self.chess_pieces[top_right].color != piece.color:
                result.append(top_right)
        # bottom-right diagonal
        if x < 8 and y < 8:
            if bottom_right not in self.chess_pieces.keys():
                result.append(bottom_right)
            elif self.chess_pieces[bottom_right].color != piece.color:
                result.append(bottom_right)
        # top-left diagonal
        if x > 1 and y > 1:
            if top_left not in self.chess_pieces.keys():
                result.append(top_left)
            elif self.chess_pieces[top_left].color != piece.color:
                result.append(top_left)
        # bottom-left diagonal
        if x > 1 and y < 8:
            if bottom_left not in self.chess_pieces.keys():
                result.append(bottom_left)
            elif self.chess_pieces[bottom_left].color != piece.color:
                result.append(bottom_left)

        top = (piece.location.x, piece.location.y - 1)
        bottom = (piece.location.x, piece.location.y + 1)
        right = (piece.location.x + 1, piece.location.y)
        left = (piece.location.x - 1, piece.location.y)

        # left side of king
        if x > 1:
            if left not in self.chess_pieces.keys():
                result.append(left)
            elif self.chess_pieces[left].color != piece.color:
                result.append(left)
        # right side of king
        if x < 8:
            if right not in self.chess_pieces.keys():
                result.append(right)
            elif self.chess_pieces[right].color != piece.color:
                result.append(right)
        # top side of king
        if y > 1:
            if top not in self.chess_pieces.keys():
                result.append(top)
            elif self.chess_pieces[top].color != piece.color:
                result.append(top)
        # bottom side of king
        if y < 8:
            if bottom not in self.chess_pieces.keys():
                result.append(bottom)
            elif self.chess_pieces[bottom].color != piece.color:
                result.append(bottom)
