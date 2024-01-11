import random
from pieces import *


class BlockGame:

    def __init__(self) -> None:
        # Can add this to the constuctor later if we wanted to create larger boards.
        self.size = 10
        self.PIECE_LIST = [P1, P2, P3, P4, P5, P6, P7, P8, P9,
                           P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24, P25, P26, P27, P28]

        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.score = 0
        self.current_pieces = [
            self.random_piece(), self.random_piece(), self.random_piece()]  # You always have 3 pieces you can choose between to play.
        self.failed_turns = 0

    def display_board(self):
        for row in self.board:
            print(' '.join("■" if cell == 1 else "□" for cell in row))

    def random_piece(self):
        return random.randint(0, len(self.PIECE_LIST) - 1)

    def is_valid_position(self, x, y):
        # Check if x coordinate is within the board boundaries
        is_x_valid = 0 <= x < self.size

        # Check if y coordinate is within the board boundaries
        is_y_valid = 0 <= y < self.size

        # Check if the cell at (x, y) is unoccupied (i.e., equals 0)
        is_cell_unoccupied = self.board[x][y] == 0

        return is_x_valid and is_y_valid and is_cell_unoccupied

    def can_place_piece(self, piece, anchor_x, anchor_y):
        piece_center = len(piece) // 2
        for i in range(len(piece)):
            for j in range(len(piece[i])):
                board_x = anchor_x + i - piece_center
                board_y = anchor_y + j - piece_center
                if piece[i][j] == 1 and not self.is_valid_position(board_x, board_y):
                    return False
        return True

    def place_piece(self, piece, anchor_x, anchor_y):
        piece_center = len(piece) // 2
        for i in range(len(piece)):
            for j in range(len(piece[i])):
                board_x = anchor_x + i - piece_center
                board_y = anchor_y + j - piece_center
                if piece[i][j] == 1:
                    if self.is_valid_position(board_x, board_y):
                        self.board[board_x][board_y] = 1
                    else:
                        return False
        return True

    def make_move(self, piece_number, x, y):

        piece = self.PIECE_LIST[self.current_pieces[piece_number]]

        if self.can_place_piece(piece, x, y):
            self.place_piece(piece, x, y)
            # replace used piece
            self.current_pieces[piece_number] = self.random_piece()
            # need to update the score. Not sure by what value.
            self.score += 0
        else:
            self.failed_turns += 1

        # then need to return the new state of the game
        return [self.board, self.current_pieces, self.score, self.failed_turns]


new_game = BlockGame()


new_game.make_move(1, 4, 5)

new_game.display_board()
