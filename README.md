*This project has been created as part of the 42 curriculum by *

# A_Maze_ing

## Description

A-Maze-ing is a terminal-based maze generator and solver written in Python 3.10+. The program reads a configuration file to set up maze parameters, generates a maze using either a Depth-First Search (DFS), embeds a visual pattern (default: "42") in the center of the maze, solves it using BFS, and renders it in the terminal with ANSI colors.

## Instructions

### Requirements

- Python 3.10 or later
- pip
- virtual-venv

### Setup and Run

````
# Step 1 — Build the virtual-venv
make venv

# Step 2 — Install dependencies in a virtualenv
make install

# Step 3 — Run the program
make run
````

### Other Commands

````
make debug        # Run in debug mode with pdb
make clean        # Remove __pycache__, .mypy_cache
make clean-venv   # Remove the virtual environment`
make lint         # Run flake8 and mypy checks
make lint-strict  # Run mypy with --strict flag
````




