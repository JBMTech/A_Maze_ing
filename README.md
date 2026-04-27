*This project has been created as part of the 42 curriculum by *

# 🧩 A_Maze_ing

## 📖 Description

A-Maze-ing is a terminal-based maze generator and solver written in Python 3.10+.
The program reads a configuration file to set up maze parameters, generates a maze
using either a Depth-First Search (DFS), embeds a visual pattern (default: "42") in
the center of the maze, solves it using BFS, and renders it in the terminal with ANSI
colors.

## ⚙️ Instructions

### Requirements

- Python 3.10 or later
- pip
- virtual-venv

### 🛠️ Setup and Run

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

## 📄 Configuration File Format

The program requires a configuration file as argument:

````
python3 a_maze_ing.py config.txt
````

**Format:** one **KEY=VALUE** per line.

````
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
````

### Parameters

| Key         | Description            |
|-------------|------------------------|
| WIDTH       | Maze width             |
| HEIGHT      | Maze height            |
| ENTRY       | Entry point (x,y)      |
| EXIT        | Exit point (x,y)       |
| OUTPUT_FILE | Output file            |
| PERFECT     | True = one path only   |

## 🧠 Algorithms
### 🔹 Maze Generation — DFS

Depth-first search (DFS) is an algorithm used to traverse or search a data
structure, such as a graph or a tree. The fundamental idea of ​​DFS is that it
explores a branch of the graph or tree as far down as possible before backtracking
to explore alternative branches.

DFS is especially useful in problems where you need to explore all possible solutions.

- Recursive backtracking
- Randomized directions
- Produces a perfect maze (tree structure)

### 🔹 Pathfinding — BFS

Depth-first search (BFS) is a graph traversal algorithm that explores a graph or tree
level by level. Starting from a specified source node, BFS visits all its immediate
neighbors before moving to the next level of nodes. This ensures that nodes at the same
depth are processed before going deeper.

BFS is useful for finding the shortest path between nodes because the first time BFS reaches
a node, it uses the shortest path. This makes BFS useful for problems such as network routing,
where the goal is to find the most efficient path between two points.

- Finds shortest path
- Guaranteed optimal solution
- Output format: N, E, S, W




