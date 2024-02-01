import random
from typing import List, Union
from pieces import *
import time


class BlockGame:
    """
    A class to represent the block puzzle game.

    Attributes:
        size (int): The size of the game board (default is 10x10).
        PIECE_LIST (list): A list of available pieces for the game.
        board (list): The current state of the game board.
        score (int): The current score of the player.
        current_pieces (list): The list of 3 pieces available to the player.
        failed_turns (int): The number of turns where the player failed to place a piece.
        game_over (bool): Indicates whether the game is over.

    Methods:
        display_board(): Prints the current state of the game board along with score and other info.
        random_piece(): Returns a random piece from the PIECE_LIST.
        is_valid_position(x, y): Checks if a position on the board is valid for placement.
        can_place_piece(piece, anchor_x, anchor_y): Checks if a piece can be placed at a given position.
        count_non_zero(lst): Counts the non-zero elements in a list.
        score_board(): Updates the score based on completed rows and columns.
        place_piece(piece, anchor_x, anchor_y): Places a piece on the board.
        is_game_over(): Checks if the game is over.
        make_move(piece_number, x, y): Makes a move in the game.
    """

    def __init__(self) -> None:
        """
        Initializes the BlockGame with a default 10x10 board and other game settings.
        """
        # Can add this to the constuctor later if we wanted to create larger boards.
        self.size = 10
        self.PIECE_LIST = PIECE_LIST
        self.reset()

    def reset(self) -> None:
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.score = 0
        self.current_pieces = [
            self.random_piece(), self.random_piece(), self.random_piece()]  # You always have 3 pieces you can choose between to play.
        self.failed_turns = 0
        self.game_over = False
        self.history = []

    def display_board(self) -> None:
        """
        Prints the current state of the board, including each cell's status, the current score, and failed turn count. 
        Displays the current pieces available for placement.
        """

        COLOURS = ["\033[31m", "\033[32m", "\u001b[33m", "\u001b[34m",
                   "\u001b[35m", "\u001b[36m", "\033[1;34m", "\033[1;31m"]
        RESET = "\033[0m"
        print('Score:', self.score, "Failed turns:", self.failed_turns)
        if self.game_over:
            print("GAME OVER MAN, GAME OVER")
        for row in self.board:
            row_str = ' '.join(
                f"{COLOURS[cell - 1]}■{RESET}" if cell > 0 else "□" for cell in row)
            print('    ', row_str)

        for row in range(5):  # Each piece is 5 rows high
            for piece_number in self.current_pieces:
                piece = self.PIECE_LIST[piece_number]
                piece_str = ' '.join(
                    f"{COLOURS[cell - 1]}■{RESET}" if cell > 0 else " " for cell in piece[row]
                )
                print(piece_str, end='  ')  # Adjust the spacing as needed
            print()  # Move to the next line after printing one row of each piece

    def random_piece(self) -> int:
        """
        Selects and returns a random piece from the available PIECE_LIST.
        """

        return random.randint(0, len(self.PIECE_LIST) - 1)

    def is_valid_position(self, x: int, y: int) -> bool:
        """
        Checks if the given position (x, y) is within the board boundaries and is empty.

        Args:
            x (int): X-coordinate on the board.
            y (int): Y-coordinate on the board.

        Returns:
            bool: True if the position is valid and empty, False otherwise.
        """
        # Check if x coordinate is within the board boundaries
        is_x_valid = 0 <= x < self.size

        # Check if y coordinate is within the board boundaries
        is_y_valid = 0 <= y < self.size

        if is_x_valid and is_y_valid:
            return self.board[x][y] == 0

        return False

    def can_place_piece(self, piece: List[List[int]], anchor_x: int, anchor_y: int) -> bool:
        """
        Determines if a piece can be placed at the given position without overlapping existing pieces.

        Args:
            piece (list): The piece to be placed.
            anchor_x (int): X-coordinate of the anchor point for the piece.
            anchor_y (int): Y-coordinate of the anchor point for the piece.

        Returns:
            bool: True if the piece can be placed, False otherwise.
        """
        piece_center = len(piece) // 2
        for i in range(len(piece)):
            for j in range(len(piece[i])):
                board_x = anchor_x + i - piece_center
                board_y = anchor_y + j - piece_center
                if piece[i][j] > 0 and not self.is_valid_position(board_x, board_y):
                    return False
        return True

    def count_non_zero(self, lst: Union[List[int], List[List[int]]]) -> int:
        """Counts the number of non-zero elements in a list. Handles both 1D and 2D lists.

            Args:
                lst (list): The list (1D or 2D) to count non-zero elements in.

            Returns:
                int: The count of non-zero elements in the list.
        """

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

    def score_board(self) -> None:
        """
        Updates the score by identifying and clearing filled rows and columns on the board. 
        The score increases based on the number of rows and columns cleared.
        """

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

    def place_piece(self, piece: List[List[int]], anchor_x: int, anchor_y: int) -> bool:
        """
        Places a piece on the board at the specified anchor position.

        Args:
            piece (list): The piece to be placed.
            anchor_x (int): X-coordinate of the anchor point for the piece.
            anchor_y (int): Y-coordinate of the anchor point for the piece.

        Returns:
            bool: True if the piece was successfully placed, False if the placement is invalid.
        """
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

    def is_game_over(self) -> bool:
        """
        Checks if there are any valid moves left. The game is over if no current pieces can be placed.

        Returns:
            bool: True if the game is over, False otherwise.
        """

        for x in range(0, self.size):
            for y in range(0, self.size):
                for piece_number in self.current_pieces:
                    piece = self.PIECE_LIST[piece_number]
                    if self.can_place_piece(piece, x, y):
                        return False
        return True

    def make_move(self, piece_number: int, x: int, y: int) -> List[Union[List[List[int]], List[int], int]]:
        """
        Processes a player's move by attempting to place a specified piece at given coordinates. 
        Updates the game state including the score and checks if the game is over.

        Args:
            piece_number (int): The index of the piece in current_pieces to be placed.
            x (int): X-coordinate of the anchor point for the piece.
            y (int): Y-coordinate of the anchor point for the piece.

        Returns:
            list: The new state of the game including the board, current pieces, score, and failed turn count.
        """

        piece = self.PIECE_LIST[self.current_pieces[piece_number]]

        if self.can_place_piece(piece, x, y):
            self.place_piece(piece, x, y)
            # replace used piece
            self.current_pieces[piece_number] = self.random_piece()
            # Score increase by 10 for each sub block fo a piece.
            self.score += self.count_non_zero(piece) * 10
            self.score_board()
            self.game_over = self.is_game_over()
        else:
            self.failed_turns += 1

        state = [self.board, self.current_pieces,
                 self.score, self.failed_turns]
        self.history.append(state)
        # then need to return the new state of the game
        return state


# new_game = BlockGame()

# while (not new_game.game_over):
#     move = new_game.make_move(
#         random.randint(0, 2), (random.randint(0, 10)), (random.randint(0, 10)))
#     print("\033c", end="")
#     new_game.display_board()
#     time.sleep(0.2)  # Adjust the delay time as needed


# # for _ in range(0, 1_000_000_000):
# #     move = new_game.make_move(
# #         random.randint(0, 2), (random.randint(0, 10)), (random.randint(0, 10)))
