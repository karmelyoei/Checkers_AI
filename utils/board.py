import pygame
from .parameters import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE, GREY
from .piece import Piece

class Board:
    def __init__(self):
        """
        Initialize the game board with pieces and their counts.
        """
        self.board = []
        self.red_left = 12
        self.white_left = 12
        self.red_kings = 0
        self.white_kings = 0
        self.new_step = None
        self.skip = None
        self.create_board()

    def draw_squares(self, win):
        """
        Draw the checkerboard squares.

        Args:
        - win: The game window.
        """
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, GREY, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate_basic(self):
        """
        Evaluation function for basic level.
        """
        return self.white_left - self.red_left

    def evaluate_intermediate(self):
        """
        Evaluation function for intermediate level.
        """
        # (self.white_kings - self.red_kings) + self.evaluate_basic()
        if len(self.skip) >= 2:
            return (self.white_kings - self.red_kings) + self.evaluate_basic() + 2
        elif len(self.skip) == 1:
            return (self.white_kings - self.red_kings) + self.evaluate_basic() + 1
        else:
            return (self.white_kings - self.red_kings) + self.evaluate_basic()

    def evaluate_advanced(self):
        """
        Evaluation function for advanced level.
        """
        if len(self.skip) >= 2:
            return (self.white_kings * 0.5 - self.red_kings * 0.5) + self.evaluate_basic() + 2
        elif len(self.skip) == 1:
            return (self.white_kings * 0.5 - self.red_kings * 0.5) + self.evaluate_basic() + 1
        else:
            return (self.white_kings * 0.5 - self.red_kings * 0.5) + self.evaluate_basic()

        #return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    def get_all_pieces(self, color):
        """
        Get all pieces of a specified color on the board.

        Args:
        - color: The color of the pieces.

        Returns:
        - List of pieces of the specified color.
        """
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        """
        Move a piece on the board.

        Args:
        - piece: The piece to move.
        - row: The destination row.
        - col: The destination column.
        """
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1


    def get_piece(self, row, col):
        """
        Get the piece at a specific position on the board.

        Args:
        - row: The row of the piece.
        - col: The column of the piece.

        Returns:
        - The piece at the specified position.
        """
        return self.board[row][col]

    def create_board(self):
        """
        Create the initial game board with pieces.
        """
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        """
        Draw the game board and pieces.

        Args:
        - win: The game window.
        """
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        """
        Remove pieces from the board.

        Args:
        - pieces: List of pieces to be removed.
        """
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        """
        Determine the winner of the game.

        Returns:
        - The winner's message or None if the game is ongoing.
        """
        if self.red_left <= 0:
            return "WHITE is Winner"
        elif self.white_left <= 0:
            return "RED is Winner"
        return None

    def get_valid_moves(self, piece):
        """
        Get all valid moves for a given piece.

        Args:
        - piece: The selected piece.

        Returns:
        - A dictionary of valid moves.
        """
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        """
        Traverse left to find valid moves.

        Args:
        - start: The starting row.
        - stop: The stopping row.
        - step: The step direction.
        - color: The color of the pieces.
        - left: The starting column.
        - skipped: List of skipped pieces.

        Returns:
        - A dictionary of valid moves.
        """
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        """
        Traverse right to find valid moves.

        Args:
        - start: The starting row.
        - stop: The stopping row.
        - step: The step direction.
        - color: The color of the pieces.
        - right: The starting column.
        - skipped: List of skipped pieces.

        Returns:
        - A dictionary of valid moves.
        """
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves
