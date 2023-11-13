# Python-Checkers-AI

## Overview
This repository contains a checkers AI implemented in Python, utilizing the minimax algorithm with Alpha-Beta pruning optimization. The game offers three difficulty levels: basic, intermediate, and advanced, each employing different evaluation functions. The depth of the game tree is set to explore 4 to 8 moves ahead.

## Difficulty Levels and Evaluation Functions
1. **Basic Level:**
    - Evaluation Function: Minimizing the number of remaining pieces on the board.

2. **Intermediate Level:**
    - Evaluation Function: Balancing the number of kings and the remaining number of pieces.

3. **Advanced Level:**
    - Evaluation Function: Assigning a score based on the number of kings, in addition to the remaining pieces.

## Players and Game Termination
- Human Player: Red
- AI Player: White

The game concludes when there are no remaining pieces on the board.and the result shows in the console. 

## User Interface
The graphical user interface (UI) of the game is developed using the pygame framework, providing an interactive and visually appealing experience.

## How to Play
1. Clone the repository to your local machine.
   ```bash
   git clone https://github.com/your-username/Python-Checkers_AI.git
   ```
2. Navigate to the project directory.
   ```bash
   cd Python-Checkers_AI
   ```
3. Install the required dependencies, including pygame.
   ```bash
   pip install -r requirements.txt
   ```
4. Run the game script.
   ```bash
   python checkers_game.py
   ```

Feel free to explore and enjoy the game! If you encounter any issues or have suggestions for improvement, please open an issue or submit a pull request.

Happy gaming! 🎮