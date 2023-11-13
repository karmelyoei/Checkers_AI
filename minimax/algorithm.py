import pygame
from copy import deepcopy
from math import inf
import sys
sys.path.append('C:\\Users\\karmel\\Desktop\\Projects\\Checkers-AI\\Checkers_AI\\utils')
from utils.parameters import WHITE, RED


def alpha_beta_ending(position, depth, alpha, beta, max_player, game, selected_option):
    """
    Alpha-beta pruning minimax algorithm with different evaluation functions based on the selected difficulty level.

    Args:
    - position: The current board position.
    - depth: The depth of the search tree.
    - alpha: The best value that the maximizing player can guarantee.
    - beta: The best value that the minimizing player can guarantee.
    - max_player: A boolean indicating whether the current player is the maximizing player.
    - game: The Game object.
    - selected_option: The selected difficulty level.

    Returns:
    - The evaluation value and the best move.
    """
    # Base case: if at the root node or the game is over, return the evaluation of the current position.
    if depth == 0 or position.winner() is not None:
        if selected_option == "Basic Level":
            return position.evaluate_basic(), position
        elif selected_option == "Intermediate Level":
            return position.evaluate_intermediate(), position
        else:
            return position.evaluate_advanced(), position

    if max_player:
        max_evaluation = -inf
        best_move = None
        for move in get_all_moves(position, WHITE):
            evaluation = alpha_beta_ending(move, depth - 1, alpha, beta, False, game, selected_option)[0]
            max_evaluation = max(max_evaluation, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                # Alpha-beta pruning for maximizing player
                break
            if max_evaluation == evaluation:
                best_move = move
        return max_evaluation, best_move
    else:
        min_evaluation = inf
        best_move = None
        for move in get_all_moves(position, RED):
            evaluation = alpha_beta_ending(move, depth - 1, alpha, beta, True, game, selected_option)[0]
            min_evaluation = min(min_evaluation, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                # Alpha-beta pruning for minimizing player
                break
            if min_evaluation == evaluation:
                best_move = move

        return min_evaluation, best_move


def simulate_move(piece, move, board, skip):
    """
    Simulates a move on the board by updating the piece's position and removing a skipped piece if applicable.

    Args:
    - piece: The piece to be moved.
    - move: The destination coordinates of the move.
    - board: The current game board.
    - skip: The piece to be skipped (if any).

    Returns:
    - The updated game board after the simulated move.
    """
    board.move(piece, move[0], move[1])
    board.skip = skip
    board.new_step = move
    if skip:
        board.remove(skip)
    return board


def get_all_moves(board, color):
    """
    Generates all possible moves for a given color on the current board.

    Args:
    - board: The current game board.
    - color: The color of the pieces for which moves are generated.

    Returns:
    - A list of all possible board positions after valid moves.
    """
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            print("skip", skip)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, skip)
            moves.append(new_board)
    return moves


def draw_moves(game, board, piece):
    """
    Draws possible moves for a given piece on the game window.

    Args:
    - game: The Game object.
    - board: The current game board.
    - piece: The selected piece.
    """
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0, 255, 0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    # pygame.time.delay(100)
