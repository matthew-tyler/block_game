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

        COLOURS = ["\033[31m", "\033[32m", "\u001b[33m", "\u001b[34m",
                   "\u001b[35m", "\u001b[36m", "\033[1;34m", "\033[1;31m"]
        RESET = "\033[0m"
        print(self.score, self.failed_turns)
        for row in self.board:
            row_str = ' '.join(
                f"{COLOURS[cell - 1]}■{RESET}" if cell > 0 else "□" for cell in row)
            print(row_str)

    def random_piece(self):
        return random.randint(0, len(self.PIECE_LIST) - 1)

    def is_valid_position(self, x, y):
        # Check if x coordinate is within the board boundaries
        is_x_valid = 0 <= x < self.size

        # Check if y coordinate is within the board boundaries
        is_y_valid = 0 <= y < self.size

        if is_x_valid and is_y_valid:
            return self.board[x][y] == 0

        return False

    def can_place_piece(self, piece, anchor_x, anchor_y):
        piece_center = len(piece) // 2
        for i in range(len(piece)):
            for j in range(len(piece[i])):
                board_x = anchor_x + i - piece_center
                board_y = anchor_y + j - piece_center
                if piece[i][j] > 0 and not self.is_valid_position(board_x, board_y):
                    return False
        return True

    def count_non_zero(self, lst):

        non_zero_count = 0
        # Check if the first element of lst is a list (indicating it's a 2D list)
        if lst and isinstance(lst[0], list):
            for row in lst:
                for cell in row:
                    if cell != 0:
                        non_zero_count += 1
        else:
            # If it's a 1D list, loop through each element
            for element in lst:
                if element != 0:
                    non_zero_count += 1

        return non_zero_count

    def score_board(self):

        rows_to_clear = []
        cols_to_clear = []

        for row in range(self.size):
            filled_cells = self.count_non_zero(self.board[row])

            if filled_cells == self.size:
                rows_to_clear.append(row)

        for col in range(self.size):
            column = [self.board[row][col] for row in range(self.size)]

            filled_cells = self.count_non_zero(column)
            if filled_cells == self.size:
                cols_to_clear.append(col)

        num_to_clear = len(rows_to_clear) + len(cols_to_clear)
        self.score += num_to_clear * (num_to_clear + 1) // 2 * 100

        for row in rows_to_clear:
            self.board[row] = [0] * self.size

        for col in cols_to_clear:
            for row in range(self.size):
                self.board[row][col] = 0

    def place_piece(self, piece, anchor_x, anchor_y):
        piece_center = len(piece) // 2
        for i in range(len(piece)):
            for j in range(len(piece[i])):
                board_x = anchor_x + i - piece_center
                board_y = anchor_y + j - piece_center
                if piece[i][j] > 0:
                    if self.is_valid_position(board_x, board_y):
                        self.board[board_x][board_y] = piece[i][j]
                    else:
                        return False
        return True

    def make_move(self, piece_number, x, y):

        piece = self.PIECE_LIST[self.current_pieces[piece_number]]

        if self.can_place_piece(piece, x, y):
            self.place_piece(piece, x, y)
            # replace used piece
            self.current_pieces[piece_number] = self.random_piece()
            # Score increase by 10 for each sub block fo a piece.
            self.score += self.count_non_zero(piece) * 10
            self.score_board()
        else:
            self.failed_turns += 1

        # then need to return the new state of the game
        return [self.board, self.current_pieces, self.score, self.failed_turns]


new_game = BlockGame()


for i in range(0, 2000):
    new_game.make_move(1, (random.randint(0, 10) + i) %
                       11, (random.randint(0, 20) + i) % 11)

new_game.display_board()
