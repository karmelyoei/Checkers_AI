import pygame
from .parameters import RED, WHITE, BLUE, SQUARE_SIZE
from .board import Board


class Game:
    def __init__(self, win):
        """
        Initialize the Game instance.

        Args:
        - win: The game window.
        """
        self._init()
        self.win = win

    def update(self):
        """
        Update the game display.

        Draws the board and valid move indicators.
        """
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        """
        Initialize game-related variables.
        """
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):
        """
        Get the winner of the game.

        Returns:
        - The winner's message or None if the game is ongoing.
        """
        return self.board.winner()

    def reset(self):
        """
        Reset the game state to the initial state.
        """
        self._init()

    def select(self, row, col):
        """
        Handle the selection of a piece on the board.

        Args:
        - row: The row of the selected piece.
        - col: The column of the selected piece.

        Returns:
        - True if a piece was successfully selected, False otherwise.
        """
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        """
        Handle the movement of a selected piece on the board.

        Args:
        - row: The destination row.
        - col: The destination column.

        Returns:
        - True if the movement was successful, False otherwise.
        """
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        """
        Draw indicators for valid moves on the board.

        Args:
        - moves: A list of valid move positions.
        """
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        """
        Change the turn to the next player.

        Clears the valid moves for the current player and switches to the other player's turn.
        """
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):
        """
        Get the current game board.

        Returns:
        - The current game board.
        """
        return self.board

    def ai_move(self, board):
        """
        Make a move on the board for the AI player.

        Args:
        - board: The new game board state after the AI's move.
        """
        self.board = board
        self.change_turn()
