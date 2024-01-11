class BlockGame:

    def __init__(self) -> None:
        # Can add this to the constuctor later if we wanted to create larger boards.
        self.size = 10
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.score = 0

    def display_board(self):
        for row in self.board:
            print(' '.join("■" if cell == 1 else "□" for cell in row))


new_game = BlockGame()

new_game.display_board()
