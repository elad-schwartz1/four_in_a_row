################################################################################
# FILE : ai.py
# WRITERS : Elad Schwartz
# DESCRIPTION: File contains AI logic for 4 in a row game. AI will search through
#              and randomly select a free column.
################################################################################

import random

class AI:
    """AI Class performs computer moves. Can be used as a rival in game instead of another person"""
    def __init__(self, game, player):
        """Constructor for AI"""
        self.empty_spaces = []
        self.game = game
        self.player = player



    def find_legal_move(self):
        """Function scans game board for empty spaces and build list of all possible free columns.
        Function then selects a random column and returns that column and the next computer move."""
        for col in range(self.game.COLUMN_NUM):
            for row in range(self.game.ROW_NUM):
                if self.game.board[row][col] == None:
                    empty_col = col
                    if empty_col not in self.empty_spaces:
                        self.empty_spaces.append(empty_col)
        random_cell = random.choice(self.empty_spaces)
        return random_cell

    def get_last_found_move(self):
        pass
