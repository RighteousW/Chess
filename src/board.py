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

        self.has_selected_piece: bool = False  # if a valid king has been clicked
        self.selected_piece: Piece = DEFAULT_PIECE  # initialised as a non-valid king

        # use every chess king's location as an index to itself in the dictionary
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
            piece_image = resize_image(piece_image_file)

            self.screen.blit(piece_image, (chess_piece.location.x * self.tile_change + 2.5,
                                           chess_piece.location.y * self.tile_change + 2.5))

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

    # on the event of west click on screen
    def left_press_at(self, location: tuple):
        x, y = location

        # convert clicked pixel coordinates to tile coordinates
        x = (x - (x % self.tile_change)) / self.tile_change
        y = (y - (y % self.tile_change)) / self.tile_change

        # if a king is already selected try to move it to the clicked tile
        if self.has_selected_piece and self.selected_piece.color == self.player_turn and in_bounds(x, y):
            if (x, y) in self.possible_places(self.selected_piece):
                is_empty_space = (x, y) not in self.chess_pieces

                # on event of en-passant
                if self.can_en_passant_to((x, y)):
                    self.chess_pieces[(x, y)] = Piece(Vector2((x, y)),
                                                      self.selected_piece.type, self.selected_piece.color)

                    # remove previous location of selected king and location of captured pawn
                    self.chess_pieces.pop((self.selected_piece.location.x, self.selected_piece.location.y))
                    self.chess_pieces.pop((x, y + 1)) if self.selected_piece.color == 'white' \
                        else self.chess_pieces.pop((x, y - 1))

                # on event of castling
                elif self.selected_piece.type == 'king' and \
                        (x == self.selected_piece.location.x - 2 or x == self.selected_piece.location.x + 2):

                    # castling west
                    if x == self.selected_piece.location.x - 2:
                        # move king to new tile
                        self.chess_pieces[(x, y)] = Piece(Vector2((x, y)),
                                                          self.selected_piece.type, self.selected_piece.color)
                        # move rook to new tile
                        self.chess_pieces[(x, y)] = Piece(Vector2((x - 1, y)),
                                                          'rook', self.selected_piece.color)
                        # remove previous location of selected king and castled rook
                        self.chess_pieces.pop((self.selected_piece.location.x, self.selected_piece.location.y))
                        self.chess_pieces.pop((1, self.selected_piece.location.y))

                    # castling east
                    elif x == self.selected_piece.location.x - 2:
                        # move king to new tile
                        self.chess_pieces[(x, y)] = Piece(Vector2((x, y)),
                                                          self.selected_piece.type, self.selected_piece.color)
                        # move rook to new tile
                        self.chess_pieces[(x, y)] = Piece(Vector2((x + 1, y)),
                                                          'rook', self.selected_piece.color)
                        # remove previous location of selected king and castled rook
                        self.chess_pieces.pop((self.selected_piece.location.x, self.selected_piece.location.y))
                        self.chess_pieces.pop((8, self.selected_piece.location.y))

                # only move if destination tile has an enemy king or is an empty tile
                elif is_empty_space or (not is_empty_space and
                                        self.chess_pieces[x, y].color != self.selected_piece.color):

                    self.chess_pieces[x, y] = Piece(Vector2(x, y), self.selected_piece.type, self.selected_piece.color)

                    # remove previous location of selected king
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
                    if (x, y) in self.chess_pieces.keys():
                        self.selected_piece = self.chess_pieces[x, y]
                    else:
                        self.has_selected_piece = False
                        self.selected_piece = DEFAULT_PIECE
            else:
                if (x, y) in self.chess_pieces.keys():
                    self.selected_piece = self.chess_pieces[x, y]
                else:
                    self.has_selected_piece = False
                    self.selected_piece = DEFAULT_PIECE

        # if no king is selected, select king at clicked tile
        elif (x, y) in self.chess_pieces:
            self.has_selected_piece = True
            self.selected_piece = self.chess_pieces[x, y]

    # returns possible locations the king can go to at current position
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
                self.bishop_movement(result, piece)
                self.rook_movement(result, piece)

            case 'king':
                self.king_movement(result, piece)
                self.king_castling(result, piece)

        return result

    def pawn_capture(self, result, pawn: Piece):
        top_right_black = (pawn.location.x - 1, pawn.location.y + 1)
        top_right_white = (pawn.location.x + 1, pawn.location.y - 1)
        top_left_black = (pawn.location.x + 1, pawn.location.y + 1)
        top_left_white = (pawn.location.x - 1, pawn.location.y - 1)

        left_white = (pawn.location.x - 1, pawn.location.y)
        right_white = (pawn.location.x + 1, pawn.location.y)
        left_black = right_white
        right_black = left_white

        # possible pieces black can capture
        if pawn.color == 'black':
            # normal captures
            if pawn.location.x > 1 and top_right_black in self.chess_pieces.keys():
                if self.chess_pieces[top_right_black].color != pawn.color:
                    result.append(top_right_black)

            if pawn.location.x < 8 and top_left_black in self.chess_pieces.keys():
                if self.chess_pieces[top_left_black].color != pawn.color:
                    result.append(top_left_black)

            # en passant
            if left_black in self.white_pawn_jump:
                result.append(top_left_black)

            elif right_black in self.white_pawn_jump:
                result.append(top_right_black)

        # possible pieces white can capture
        elif pawn.color == 'white':
            # normal captures
            if pawn.location.x > 1 and top_left_white in self.chess_pieces.keys():
                if self.chess_pieces[top_left_white].color != pawn.color:
                    result.append(top_left_white)

            if pawn.location.x < 8 and top_right_white in self.chess_pieces.keys():
                if self.chess_pieces[top_right_white].color != pawn.color:
                    result.append(top_right_white)

            # en passant
            if left_white in self.black_pawn_jump:
                result.append(top_left_white)

            if right_white in self.black_pawn_jump:
                result.append(top_right_white)

        return result

    def pawn_movement(self, result, pawn: Piece):
        one_white = (pawn.location.x, pawn.location.y - 1)  # 1 tile in front of king
        one_black = (pawn.location.x, pawn.location.y + 1)
        two_white = (pawn.location.x, pawn.location.y - 2)  # 2 tiles in front of king
        two_black = (pawn.location.x, pawn.location.y + 2)

        # first pawn movement, able to move two spaces
        if not pawn.has_moved:
            if (pawn.color == 'black' and
                    two_black not in self.chess_pieces.keys() and
                    one_black not in self.chess_pieces.keys()):
                result.append(two_black)
            elif (pawn.color == 'white' and
                  two_white not in self.chess_pieces.keys() and
                  one_white not in self.chess_pieces.keys()):
                result.append(two_white)

        # normal pawn movement
        if pawn.color == 'black' and one_black not in self.chess_pieces.keys():
            result.append(one_black)
        elif pawn.color == 'white' and one_white not in self.chess_pieces.keys():
            result.append(one_white)

    def rook_movement(self, result, rook: Piece):
        x = int(rook.location.x)
        y = int(rook.location.y)

        # west side of rook
        if x > 1:
            for _ in range(1, x):
                if (rook.location.x - _, rook.location.y) in self.chess_pieces.keys():
                    if self.chess_pieces[rook.location.x - _, rook.location.y].color != rook.color:
                        result.append((rook.location.x - _, rook.location.y))
                    break
                result.append((rook.location.x - _, rook.location.y))

        # east side of rook
        if x < 8:
            for _ in range(x + 1, 9):
                if (_, rook.location.y) in self.chess_pieces.keys():
                    if self.chess_pieces[_, rook.location.y].color != rook.color:
                        result.append((_, rook.location.y))
                    break
                result.append((_, rook.location.y))

        # north side of rook
        if y > 1:
            for _ in range(1, y):
                if (rook.location.x, rook.location.y - _) in self.chess_pieces.keys():
                    if self.chess_pieces[rook.location.x, rook.location.y - _].color != rook.color:
                        result.append((rook.location.x, rook.location.y - _))
                    break
                result.append((rook.location.x, rook.location.y - _))

        # south side of rook
        if y < 8:
            for _ in range(y + 1, 9):
                if (rook.location.x, _) in self.chess_pieces.keys():
                    if self.chess_pieces[rook.location.x, _].color != rook.color:
                        result.append((rook.location.x, _))
                    break
                result.append((rook.location.x, _))

    def knight_movement(self, result, knight: Piece):
        x = int(knight.location.x)
        y = int(knight.location.y)

        if x < 7 and y > 1:  # east-east-up
            if (knight.location.x + 2, knight.location.y - 1) not in self.chess_pieces.keys():
                result.append((knight.location.x + 2, knight.location.y - 1))
            elif self.chess_pieces[(knight.location.x + 2, knight.location.y - 1)].color != knight.color:
                result.append((knight.location.x + 2, knight.location.y - 1))

        if x < 7 and y < 8:  # east-east-down
            if (knight.location.x + 2, knight.location.y + 1) not in self.chess_pieces.keys():
                result.append((knight.location.x + 2, knight.location.y + 1))
            elif self.chess_pieces[(knight.location.x + 2, knight.location.y + 1)].color != knight.color:
                result.append((knight.location.x + 2, knight.location.y + 1))

        if x > 2 and y > 1:  # west-west-up
            if (knight.location.x - 2, knight.location.y - 1) not in self.chess_pieces.keys():
                result.append((knight.location.x - 2, knight.location.y - 1))
            elif self.chess_pieces[(knight.location.x - 2, knight.location.y - 1)].color != knight.color:
                result.append((knight.location.x - 2, knight.location.y - 1))

        if x > 2 and y < 8:  # west-west-down
            if (knight.location.x - 2, knight.location.y + 1) not in self.chess_pieces.keys():
                result.append((knight.location.x - 2, knight.location.y + 1))
            elif self.chess_pieces[(knight.location.x - 2, knight.location.y + 1)].color != knight.color:
                result.append((knight.location.x - 2, knight.location.y + 1))

        if x < 8 and y > 2:  # up-up-east
            if (knight.location.x + 1, knight.location.y - 2) not in self.chess_pieces.keys():
                result.append((knight.location.x + 1, knight.location.y - 2))
            elif self.chess_pieces[(knight.location.x + 1, knight.location.y - 2)].color != knight.color:
                result.append((knight.location.x + 1, knight.location.y - 2))

        if x > 1 and y > 2:  # up-up-west
            result.append((knight.location.x - 1, knight.location.y - 2))
            if (knight.location.x - 1, knight.location.y - 2) not in self.chess_pieces.keys():
                result.append((knight.location.x - 1, knight.location.y - 2))
            elif self.chess_pieces[(knight.location.x - 1, knight.location.y - 2)].color != knight.color:
                result.append((knight.location.x - 1, knight.location.y - 2))

        if x < 8 and y < 7:  # down-down-east
            if (knight.location.x + 1, knight.location.y + 2) not in self.chess_pieces.keys():
                result.append((knight.location.x + 1, knight.location.y + 2))
            elif self.chess_pieces[(knight.location.x + 1, knight.location.y + 2)].color != knight.color:
                result.append((knight.location.x + 1, knight.location.y + 2))

        if x > 1 and y < 7:  # down-down-west
            if (knight.location.x - 1, knight.location.y + 2) not in self.chess_pieces.keys():
                result.append((knight.location.x - 1, knight.location.y + 2))
            elif self.chess_pieces[(knight.location.x - 1, knight.location.y + 2)].color != knight.color:
                result.append((knight.location.x - 1, knight.location.y + 2))

    def bishop_movement(self, result, bishop: Piece):
        x = int(bishop.location.x)
        y = int(bishop.location.y)

        # north-east diagonal
        if x < 8 and y > 1:
            for _ in range(1, 9 - np.minimum(x, y)):
                if (bishop.location.x + _, bishop.location.y - _) in self.chess_pieces.keys():
                    if self.chess_pieces[bishop.location.x + _, bishop.location.y - _].color != bishop.color:
                        result.append((bishop.location.x + _, bishop.location.y - _))
                    break
                result.append((bishop.location.x + _, bishop.location.y - _))

        # south-east diagonal
        if x < 8 and y < 8:
            for _ in range(1, np.maximum(9 - x, y - 1)):
                if (bishop.location.x + _, bishop.location.y + _) in self.chess_pieces.keys():
                    if self.chess_pieces[bishop.location.x + _, bishop.location.y + _].color != bishop.color:
                        result.append((bishop.location.x + _, bishop.location.y + _))
                    break
                result.append((bishop.location.x + _, bishop.location.y + _))

        # north-west diagonal
        if x > 1 and y > 1:
            for _ in range(1, np.minimum(x, y)):
                if (bishop.location.x - _, bishop.location.y - _) in self.chess_pieces.keys():
                    if self.chess_pieces[bishop.location.x - _, bishop.location.y - _].color != bishop.color:
                        result.append((bishop.location.x - _, bishop.location.y - _))
                    break
                result.append((bishop.location.x - _, bishop.location.y - _))

        # south-west diagonal
        if x > 1 and y < 8:
            for _ in range(1, np.maximum(x, y)):
                if (bishop.location.x - _, bishop.location.y + _) in self.chess_pieces.keys():
                    if self.chess_pieces[bishop.location.x - _, bishop.location.y + _].color != bishop.color:
                        result.append((bishop.location.x - _, bishop.location.y + _))
                    break
                result.append((bishop.location.x - _, bishop.location.y + _))

    def king_movement(self, result, king: Piece):
        x = int(king.location.x)
        y = int(king.location.y)

        top_right = (king.location.x + 1, king.location.y - 1)
        top_left = (king.location.x - 1, king.location.y - 1)
        bottom_left = (king.location.x - 1, king.location.y + 1)
        bottom_right = (king.location.x + 1, king.location.y + 1)

        #  north-east diagonal
        if x < 8 and y > 1:
            if top_right not in self.chess_pieces.keys():
                result.append(top_right)
            elif self.chess_pieces[top_right].color != king.color:
                result.append(top_right)
        # south-east diagonal
        if x < 8 and y < 8:
            if bottom_right not in self.chess_pieces.keys():
                result.append(bottom_right)
            elif self.chess_pieces[bottom_right].color != king.color:
                result.append(bottom_right)
        # north-west diagonal
        if x > 1 and y > 1:
            if top_left not in self.chess_pieces.keys():
                result.append(top_left)
            elif self.chess_pieces[top_left].color != king.color:
                result.append(top_left)
        # south-west diagonal
        if x > 1 and y < 8:
            if bottom_left not in self.chess_pieces.keys():
                result.append(bottom_left)
            elif self.chess_pieces[bottom_left].color != king.color:
                result.append(bottom_left)

        north = (king.location.x, king.location.y - 1)
        south = (king.location.x, king.location.y + 1)
        east = (king.location.x + 1, king.location.y)
        west = (king.location.x - 1, king.location.y)

        # west side of king
        if x > 1:
            if west not in self.chess_pieces.keys():
                result.append(west)
            elif self.chess_pieces[west].color != king.color:
                result.append(west)
        # east side of king
        if x < 8:
            if east not in self.chess_pieces.keys():
                result.append(east)
            elif self.chess_pieces[east].color != king.color:
                result.append(east)
        # north side of king
        if y > 1:
            if north not in self.chess_pieces.keys():
                result.append(north)
            elif self.chess_pieces[north].color != king.color:
                result.append(north)
        # south side of king
        if y < 8:
            if south not in self.chess_pieces.keys():
                result.append(south)
            elif self.chess_pieces[south].color != king.color:
                result.append(south)

    def king_castling(self, result, king: Piece):
        if king.has_moved:
            return None

        # castling west
        if (1, king.location.y) in self.chess_pieces.keys():
            if (self.chess_pieces[(1, king.location.y)].type == 'rook' and
                    self.chess_pieces[(1, king.location.y)].color == king.color and
                    not self.chess_pieces[(1, king.location.y)].has_moved):
                # if there is a piece between king and rook quit method
                for _ in range(2, 5):
                    if (_, king.location.y) in self.chess_pieces.keys():
                        return None
                result.append((king.location.x - 2, king.location.y))
                print(f'{king.color} can castle west')

        # castling east for white
        if (8, king.location.y) in self.chess_pieces.keys():
            if self.chess_pieces[(8, king.location.y)].type == 'rook' and \
                    not self.chess_pieces[(8, king.location.y)].has_moved:
                # if there is a piece between king and rook quit method
                for _ in range(6, 8):
                    if (_, king.location.y) in self.chess_pieces.keys():
                        return None
                result.append((king.location.x + 2, king.location.y))
                print(f'{king.color} can castle east')

    # returns if en passant is possible
    def can_en_passant_to(self, location) -> bool:
        # return false if selected king is not a pawn or can't go to destination tile
        if self.selected_piece.type != 'pawn' or location not in self.possible_places(self.selected_piece):
            return False

        x, y = location
        if self.selected_piece.color == 'white':
            # return false if king below destination tile not in list of all king locations
            if (x, y + 1) not in self.chess_pieces.keys():
                return False
            # return true if king below destination tile in list of recently jumped enemy pieces
            if (x, y + 1) in self.black_pawn_jump:
                return True
            return False

        elif self.selected_piece.color == 'black':
            # return false if king below destination tile not in list of all king locations
            if (x, y - 1) not in self.chess_pieces.keys():
                return False
            # return true if king below destination tile in list of recently jumped enemy pieces
            if (x, y - 1) in self.white_pawn_jump:
                return True
            return False
        return False
