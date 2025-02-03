"""Basic minesweeper implemented in python for easy testing of various solvers and algorithms.

This module provides the `MineSweeper` class. It requires `numpy` and `matplotlib`.
"""

import numpy as np
from matplotlib.image import imread

class MineSweeper:
    """
    Class with basic minesweeper board generation, gameplay and utilities.

    Use methods `fromdimensions` and `fromPNG` to create new instances of this class.
    To display a board in ascii simply `print` an instance of this class.

    Other methods are:
        `reveal`
        `getstate`
        `getsquare`

    Those methods provide computer programs with the same abilities any human player would have.
    """

    def __init__(self, mines:np.ndarray):
        self.mines = np.asarray(mines > 0, dtype=np.int8)
        self.size = self.mines.shape
        self.num_mines = np.sum(self.mines)
        self.board = np.empty(self.size, dtype=np.int8)
        self.covered = np.ones(self.size, dtype=np.int8)
        self.num_covered = self.size[0]*self.size[1]
        self.game_state = 'in_progress'

        for r in range(self.size[0]):
            self.board[r, :] = np.convolve(self.mines[r, :], [1, 1, 1], 'same')
        for c in range(self.size[1]):
            self.board[:, c] = np.convolve(self.board[:, c], [1, 1, 1], 'same')

    @classmethod
    def fromdimensions(cls, board_dims:tuple[int, int], num_mines:int):
        """
        Generate a board with board dimensions `(rows, columns)` and `num_mines` mines.
        """
        mines = np.zeros(board_dims, dtype=np.int8)

        mine_indices = np.random.choice(board_dims[0]*board_dims[1], num_mines, replace=False)
        for i in range(num_mines):
            mines[mine_indices[i]//board_dims[1], mine_indices[i]%board_dims[1]] = 1

        return cls(mines)

    @classmethod
    def fromPNG(cls, image_path:str):
        """
        Generate board from an RGB PNG file, where white pixels are safe and black are mines.
        """
        im_data = imread(image_path)

        mines = 1 - np.asarray(im_data[:, :, 0], dtype=np.int8)

        return cls(mines)

    def __str__(self):
        out = "\n"
        for r in range(self.size[0]):
            out += "|"
            for c in range(self.size[1]):
                if self.covered[r, c]:
                    out += " ."
                elif self.mines[r, c]:
                    out += " X"
                elif self.board[r, c]:
                    out += f" {self.board[r, c]}"
                else:
                    out += "  "
            out += " |\n"
        return out
    
    def reveal(self, row:int, col:int) -> int:
        """
        Reveal a square and return the result. Return values:
        `-1`: Square out of bounds or already revealed
        `1`: Square revealed, not a mine
        `0`: Mine revealed, game lost
        """
        if row < 0 or self.size[0] <= row or col < 0 or self.size[1] <= col or self.covered[row, col] == 0:
            return -1
        
        self.covered[row, col] = 0
        self.num_covered -= 1
        if self.num_covered == self.num_mines:
            self.game_state = 'win'

        if self.mines[row, col]:
            self.game_state = 'failure'
            return 0

        if self.board[row, col] == 0:
            self.reveal(row-1, col-1)
            self.reveal(row-1, col  )
            self.reveal(row-1, col+1)
            self.reveal(row,   col-1)
            self.reveal(row,   col+1)
            self.reveal(row+1, col-1)
            self.reveal(row+1, col  )
            self.reveal(row+1, col+1)

        return 1
    
    def getstate(self) -> str:
        """
        Possible game states are `'in_progress'`, `'failure'` and `'win'`.
        """
        return self.game_state
    
    def getsquare(self, row:int, col:int) -> int:
        """
        Return a code indicating the value of the square:
        `0-8`: normal uncovered square with a number of adjacent mines
        `-1` : covered square
        `-2` : mine
        `-3` : out of bounds
        """

        if row < 0 or self.size[0] <= row or col < 0 or self.size[1] <= col:
            return -3

        if self.covered[row, col]:
            return -1
        
        if self.mines[row, col]:
            return -2
        
        return self.board[row, col]