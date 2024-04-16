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

        self.has_selected_piece: bool = False  # if a valid piece has been clicked
        self.selected_piece: Piece = DEFAULT_PIECE  # initialised as a non-valid piece

        # use every chess piece's location as an index to itself in the dictionary
        self.chess_pieces: dict[(int, int):Piece] = dict()

        # determines who plays
        self.player_turn: str = 'white'

        # contains pawns that have recently jumped a tile
        self.black_pawn_jump: list[tuple] = list()
        self.white_pawn_jump: list[tuple] = list()

        self.initialize_pieces()

        self.tile_change: float = SCREEN_HEIGHT / 10  # distance between tiles in pixels

    # initial positions of chess_pieces
    def initialize_pieces(self):

        # initialize pawns
        for _ in range(1, 9):
            self.chess_pieces[_, 2] = Piece(Vector2(_, 2), 'pawn', 'black')
            self.chess_pieces[_, 7] = Piece(Vector2(_, 7), 'pawn', 'white')

        # initialize rooks
        self.chess_pieces[1, 1] = Piece(Vector2(1, 1), 'rook', 'black')
        self.chess_pieces[8, 1] = Piece(Vector2(8, 1), 'rook', 'black')
        self.chess_pieces[1, 8] = Piece(Vector2(1, 8), 'rook', 'white')
        self.chess_pieces[8, 8] = Piece(Vector2(8, 8), 'rook', 'white')

        # initialize knights
        self.chess_pieces[2, 1] = Piece(Vector2(2, 1), 'knight', 'black')
        self.chess_pieces[7, 1] = Piece(Vector2(7, 1), 'knight', 'black')
        self.chess_pieces[2, 8] = Piece(Vector2(2, 8), 'knight', 'white')
        self.chess_pieces[7, 8] = Piece(Vector2(7, 8), 'knight', 'white')

        # initialize bishops
        self.chess_pieces[3, 1] = Piece(Vector2(3, 1), 'bishop', 'black')
        self.chess_pieces[6, 1] = Piece(Vector2(6, 1), 'bishop', 'black')
        self.chess_pieces[3, 8] = Piece(Vector2(3, 8), 'bishop', 'white')
        self.chess_pieces[6, 8] = Piece(Vector2(6, 8), 'bishop', 'white')

        # initialize queens
        self.chess_pieces[4, 1] = Piece(Vector2(4, 1), 'queen', 'black')
        self.chess_pieces[4, 8] = Piece(Vector2(4, 8), 'queen', 'white')

        # initialize kings
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
                                 Rect(x * self.tile_change, y * self.tile_change, self.tile_change, self.tile_change))

    # draw lines on tile borders that makes the tiles more distinct
    def draw_lines(self):
        for _ in range(1, 10):
            # horizontal lines
            pygame.draw.line(self.screen, COLOR_WHITE,
                             (self.tile_change, _ * self.tile_change),
                             (self.tile_change * 9, _ * self.tile_change))

            # vertical lines
            pygame.draw.line(self.screen, COLOR_WHITE,
                             (_ * self.tile_change, self.tile_change),
                             (_ * self.tile_change, self.tile_change * 9))

    # draw images of chess_pieces
    def draw_chess_pieces(self):
        for chess_piece in self.chess_pieces.values():
            piece_image_file = CHESS_PIECE_IMAGES[f'{chess_piece.type}_{chess_piece.color}']
            piece_image = resize_image(piece_image_file, 40)

            self.screen.blit(piece_image, (chess_piece.location.x * self.tile_change + 10,
                                           chess_piece.location.y * self.tile_change + 10))

    # changes tile color of focused tile to cyan and tiles it can move to as light cyan
    def draw_focused_piece(self):
        # check if selected tile is valid
        if self.selected_piece != DEFAULT_PIECE:

            # make color of selected tile cyan
            pygame.draw.rect(self.screen, COLOR_SELECTED_PIECE,
                             Rect(self.selected_piece.location.x * self.tile_change,
                                  self.selected_piece.location.y * self.tile_change,
                                  self.tile_change,
                                  self.tile_change))

            # make color of possible tiles light cyan
            for (x, y) in self.possible_places(self.selected_piece):
                pygame.draw.rect(self.screen, COLOR_POSSIBLE_TILES,
                                 Rect(x * self.tile_change,
                                      y * self.tile_change,
                                      self.tile_change,
                                      self.tile_change))

    # renders the board, the borderlines and chess_pieces
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
        x = (x - (x % self.tile_change)) / self.tile_change
        y = (y - (y % self.tile_change)) / self.tile_change

        # if a piece is already selected try to move it to the clicked tile
        if self.has_selected_piece and self.selected_piece.color == self.player_turn and in_bounds(x, y):
            if (x, y) in self.possible_places(self.selected_piece):
                is_empty_space = (x, y) not in self.chess_pieces

                # on event of en-passant
                if self.can_en_passant_to((x, y)):
                    self.chess_pieces[(x, y)] = Piece(Vector2((x, y)),
                                                      self.selected_piece.type, self.selected_piece.color)

                    # remove previous location of selected piece and location of captured pawn
                    self.chess_pieces.pop((self.selected_piece.location.x, self.selected_piece.location.y))
                    if self.selected_piece.color == 'white':
                        self.chess_pieces.pop((x, y + 1))
                    else:
                        self.chess_pieces.pop((x, y - 1))

                # only move if destination tile has an enemy piece or is an empty tile
                elif is_empty_space or (not is_empty_space and
                                        self.chess_pieces[x, y].color != self.selected_piece.color):

                    self.chess_pieces[x, y] = Piece(Vector2(x, y), self.selected_piece.type, self.selected_piece.color)

                    # remove previous location of selected piece
                    self.chess_pieces.pop((self.selected_piece.location.x, self.selected_piece.location.y))

                    # keeping location of pawn that moved two spaces on first move, info needed for en passant
                    if (self.selected_piece.type == 'pawn' and
                            self.selected_piece.location.y == 2 or
                            self.selected_piece.location.y == 7):

                        if self.selected_piece.color == 'white':
                            if y == self.selected_piece.location.y - 2:
                                self.white_pawn_jump.append((x, y))

                        if self.selected_piece.color == 'black':
                            if y == self.selected_piece.location.y + 2:
                                self.black_pawn_jump.append((x, y))

                    # only allow en passant on opponents first move following pawn jump
                    if self.selected_piece.color == 'white':
                        self.black_pawn_jump.clear()
                    if self.selected_piece.color == 'black':
                        self.white_pawn_jump.clear()

                    self.has_selected_piece = False
                    self.selected_piece = DEFAULT_PIECE
                    self.chess_pieces[x, y].has_moved = True
                    self.switch_player()
                else:
                    self.has_selected_piece = False
                    self.selected_piece = DEFAULT_PIECE
            else:
                self.has_selected_piece = False
                self.selected_piece = DEFAULT_PIECE

        # if no piece is selected, select piece at clicked tile
        elif (x, y) in self.chess_pieces:
            self.has_selected_piece = True
            self.selected_piece = self.chess_pieces[x, y]

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
        top_right_black = (pawn_piece.location.x - 1, pawn_piece.location.y + 1)
        top_right_white = (pawn_piece.location.x + 1, pawn_piece.location.y - 1)
        top_left_black = (pawn_piece.location.x + 1, pawn_piece.location.y + 1)
        top_left_white = (pawn_piece.location.x - 1, pawn_piece.location.y - 1)

        left_white = (pawn_piece.location.x - 1, pawn_piece.location.y)
        right_white = (pawn_piece.location.x + 1, pawn_piece.location.y)
        left_black = right_white
        right_black = left_white

        # possible pieces black can capture
        if pawn_piece.color == 'black':
            # normal captures
            if pawn_piece.location.x > 1 and top_right_black in self.chess_pieces.keys():
                if self.chess_pieces[top_right_black].color != pawn_piece.color:
                    result.append(top_right_black)

            if pawn_piece.location.x < 8 and top_left_black in self.chess_pieces.keys():
                if self.chess_pieces[top_left_black].color != pawn_piece.color:
                    result.append(top_left_black)

            # en passant
            if left_black in self.white_pawn_jump:
                result.append(top_left_black)

            elif right_black in self.white_pawn_jump:
                result.append(top_right_black)

        # possible pieces white can capture
        elif pawn_piece.color == 'white':
            # normal captures
            if pawn_piece.location.x > 1 and top_left_white in self.chess_pieces.keys():
                if self.chess_pieces[top_left_white].color != pawn_piece.color:
                    result.append(top_left_white)

            if pawn_piece.location.x < 8 and top_right_white in self.chess_pieces.keys():
                if self.chess_pieces[top_right_white].color != pawn_piece.color:
                    result.append(top_right_white)

            # en passant
            if left_white in self.black_pawn_jump:
                result.append(top_left_white)

            if right_white in self.black_pawn_jump:
                result.append(top_right_white)

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

    # returns if en passant is possible
    def can_en_passant_to(self, location) -> bool:
        # return false if selected piece is not a pawn or can't go to destination tile
        if self.selected_piece.type != 'pawn' or location not in self.possible_places(self.selected_piece):
            return False

        x, y = location
        if self.selected_piece.color == 'white':
            # return false if piece below destination tile not in list of all piece locations
            if (x, y + 1) not in self.chess_pieces.keys():
                return False
            # return true if piece below destination tile in list of recently jumped enemy pieces
            if (x, y + 1) in self.black_pawn_jump:
                return True
            return False

        elif self.selected_piece.color == 'black':
            # return false if piece below destination tile not in list of all piece locations
            if (x, y - 1) not in self.chess_pieces.keys():
                return False
            # return true if piece below destination tile in list of recently jumped enemy pieces
            if (x, y - 1) in self.white_pawn_jump:
                return True
            return False
        return False
