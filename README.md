# MancalaProject
This project implements a full simulation environment for the game Mancala, including:

A complete game engine

A Minimax AI with adjustable lookahead depth

A batch simulator that plays large numbers of games

A Jupyter Notebook Scratchpad for experiments, graphs, and analysis

This setup is used to test how AI depth affects performance (e.g., 2-ply vs 5-ply vs 10-ply).

├── MancalaGame.py       # Full Mancala rules + board logic

├── MinimaxAI.py         # Minimax implementation with heuristic + recursion

├── PlayGames.py         # Runs batches of games for experiments

├── Scratchpad.ipynb     # Notebook for analysis & plotting

└── README.md

1. MancalaGame.py — The Game Engine

This file implements:

The Mancala board (pits, mancala stores, turn tracking)

How stones move and wrap around the board

Valid move checking

Capture rules

End-game detection

Final score calculation

display_board() for debugging visualization

2. MinimaxAI.py — The AI Player

This file implements:

A configurable-depth Minimax search

A simple heuristic:
(your mancala score − opponent mancala score)

Recursion + deep copying of game states

Move selection using choose_move()

3. PlayGames.py — Running Experiments

PlayGames runs multiple complete games automatically.

Player types:

"random" — chooses from valid moves at random

"minimax" — uses the Minimax AI

4. Scratchpad.ipynb — How to Use It

This notebook is your workspace for:

Running experiments

Testing AI depths

Visualizing win percentages
