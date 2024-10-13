Project: AI Application in 2048 Game
This project applies AI to the 2048 game using Pygame. The game is implemented with two AI algorithms: Minimax and Expectimax, which are used to predict the next best move and potential future moves in this highly unpredictable game.

Game Modes:
Human Mode: The player controls the game.
AI Mode: The AI, powered by Minimax and Expectimax algorithms, autonomously plays the game and determines the optimal moves.
AI Algorithms:
Minimax Algorithm: This algorithm evaluates the game state to minimize the possible loss while maximizing the AI’s score by considering all possible moves.
Expectimax Algorithm: This algorithm is particularly well-suited for handling randomness, such as the unpredictability in spawning new tiles in the 2048 game. Expectimax is used to predict the potential outcomes of future moves and make decisions accordingly.
Player Prediction Feature:
To add an AI element to the Human Mode, a heuristic function is included to predict the maximum score a player might achieve until the game ends (losing is more likely than winning for an average player). This prediction is calculated after the player's first 10 moves.

The heuristic function is based on:

The largest tile on the board.
The number of empty (void) tiles.
The arrangement of tiles (whether the larger tiles are grouped well).
