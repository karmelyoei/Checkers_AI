import pygame
import sys
from math import inf
from utils.parameters import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, GREEN, FPS
from utils.game import Game
from minimax.algorithm import alpha_beta_ending

# Create the main window
screen_one = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")

# Create the Second Window
screen_two = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.init()
pygame.font.init()

# Fonts
title_font = pygame.font.Font("assets/Cheri400.ttf", 100)
button_font = pygame.font.Font("assets/Cheri400.ttf", 28)

# Drop-down menu options
options = ["Basic Level", "Intermediate Level", "Advance Level"]
selected_option = None  # Initialize to None


def get_row_col_from_mouse(pos):
    """Convert mouse position to row and column on the board."""
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    """Main function to run the game."""
    global selected_option
    run = True
    clock = pygame.time.Clock()
    game = Game(screen_two)
    depth = 2

    # Main loop
    running = True
    while running:
        screen_one.fill(GREEN)

        # Draw title
        title_text = title_font.render("Checker", True, RED)
        screen_one.blit(title_text, (WIDTH // 2 + 40 - title_text.get_width() // 2, 50))

        # Draw  three buttons for game levels
        pygame.draw.rect(screen_one, WHITE, (285, 250, 300, 70), 2)
        option_button1 = button_font.render(options[0], True, WHITE)
        screen_one.blit(option_button1, (360, 270))

        pygame.draw.rect(screen_one, WHITE, (285, 380, 300, 70), 2)
        option_button2 = button_font.render(options[1], True, WHITE)
        screen_one.blit(option_button2, (300, 400))

        pygame.draw.rect(screen_one, WHITE, (285, 500, 300, 70), 2)
        option_button3 = button_font.render(options[2], True, WHITE)
        screen_one.blit(option_button3, (330, 510))

        # Event handling for buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if option_button1.get_rect(x=360, y=270).collidepoint(pygame.mouse.get_pos()):
                    print("Selected the Basic level")
                    selected_option = options[0]
                    running = False  # Exit the button handling loop
                elif option_button2.get_rect(x=300, y=400).collidepoint(pygame.mouse.get_pos()):
                    print("Selected the Intermediate level")
                    selected_option = options[1]
                    running = False  # Exit the button handling loop
                elif option_button3.get_rect(x=330, y=510).collidepoint(pygame.mouse.get_pos()):
                    print("Selected the Advances level")
                    selected_option = options[2]
                    running = False  # Exit the button handling loop

        # Update the display
        pygame.display.flip()
        # Cap the frame rate
        pygame.time.Clock().tick(FPS)

    # Game loop
    while run:
        clock.tick(FPS)
        if game.winner() is not None:
            print(game.winner())
            break

        if game.turn == WHITE:
            value, new_board = alpha_beta_ending(game.get_board(), depth, -inf, inf, WHITE, game, selected_option)
            game.ai_move(new_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()


if __name__ == '__main__':
    main()
