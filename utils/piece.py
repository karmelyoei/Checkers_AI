# Import necessary constants and modules
from .parameters import SQUARE_SIZE, GREY, CROWN
import pygame


class Piece:
    # Class constants for padding and outline of the piece
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        """
        Initialize a Piece instance.

        Args:
        - row: The row position on the board.
        - col: The column position on the board.
        - color: The color of the piece.
        """
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        """
        Calculate the screen position (x, y) based on the row and column.
        """
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        """
        Make the piece a king.
        """
        self.king = True

    def draw(self, win):
        """
        Draw the piece on the game window.

        Args:
        - win: The game window.
        """
        # Calculate radius and draw the circle representing the piece
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)

        # If the piece is a king, draw the crown on top
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row, col):
        """
        Move the piece to a new position.

        Args:
        - row: The new row position.
        - col: The new column position.
        """
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        """
        String representation of the Piece instance.

        Returns:
        - A string representing the color of the piece.
        """
        return str(self.color)
