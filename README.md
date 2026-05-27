*This project has been created as part of the 42 curriculum by jabuleje and mvasquez*

# 🧩 A_Maze_ing

## 📖 Description

**A-Maze-ing** is a maze generator and solver written in Python 3.10+.
It reads a configuration file, generates a maze based on given parameters,
and displays it in the terminal using ASCII rendering and ANSI colors.

The project also provides a **reusable Python module (`mazegen`)** that allows
maze generation and solving in other projects.

Main features:

- Random maze generation (DFS-based)
- Optional perfect maze (single solution)
- Embedded "42" pattern inside the maze
- Shortest path resolution using BFS
- ASCII visualization with colors
- Export to file using hexadecimal encoding

---

## ⚙️ Instructions

### Requirements

- Python 3.10 or later
- pip
- virtualenv (recommended)

---

### 🛠️ Setup and Run

````bash
# Step 1 — Create virtual environment
make venv

# Step 2 — Install dependencies
make install

# Step 3 — Run the program
make run
````

### Other Commands

````bash
make debug        # Run in debug mode with pdb
make clean        # Remove __pycache__, .mypy_cache
make clean-venv   # Remove the virtual environment`
make lint         # Run flake8 and mypy checks
make lint-strict  # Run mypy with --strict flag
````

### ▶️ Usage

````bash
python3 a_maze_ing.py config.txt
````

The program will display an interactive menu:

- Generate maze
- Show solution
- Hide solution
- Change wall color
- Exit

## 📄 Configuration File Format

The configuration file must contain one **`KEY=VALUE`** per line.

Example:

````bash
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEEd=42
````

### Parameters

| Key         | Description            |
|-------------|------------------------|
| WIDTH       | Maze width             |
| HEIGHT      | Maze height            |
| ENTRY       | Entry point (x,y)      |
| EXIT        | Exit point (x,y)       |
| OUTPUT_FILE | Output file name       |
| PERFECT     | True = one path only   |
| SEED        | Optional random seed   |

## 🧠 Algorithms

### 🔹 Maze Generation — DFS

The maze is generated using a randomized Depth-First Search (DFS):

- Starts from the entry point
- Randomly explores neighbors
- Removes walls between connected cells
- Backtracks when no unvisited neighbors remain

This produces a *perfect maze (tree structure)*.

### 🔹 Pathfinding — BFS

The shortest path is computed using Breadth-First Search (BFS):

- Explores nodes level by level
- Guarantees shortest path
- Reconstructs path using parent tracking

Output format:

````
N, E, S, W
````

## 🧱 Maze Representation

Each cell is encoded using a hexadecimal value representing walls:

| Bit         | Direction      |
|-------------|----------------|
| 0           | North          |
| 1           | East           |
| 2           | South          |
| 3           | West           |

Example:

- A (1010) -> East and West walls closed
- 3 (0011) -> Noth and East closed

---

## 🎨 Visual Representation

The maze is displayed in the terminal using:

- ASCII walls (████, █)
- ANSI colors:
    - Walls (customizable)
    - Entry (E)
    - Exit (X)
    - Solution path (●)
    - "42" pattern

---

## ♻️ Reusable Module — mazegen

The proyect includes a reusable module:

````python
from mazegen.maze_generator import MazeGenerator
````

Example:

````python
config = {
    "WIDTH": 20,
    "HEIGHT": 15,
    "ENTRY": (0, 0),
    "EXIT": (19, 14),
    "PERFECT": True,
    "SEED": 42
}

maze = MazeGenerator(config)
maze.generate()
maze.solve()
maze.print_maze(show_path=True)
````

### Features

- Generate maze (generate)
- Solve maze (solve)
- Print ASCII (print_maze)
- Export to file (write_maze)

## 🧩 Design Choices

### Why DFS?

- Simple to implement
- Produces natural-looking mazes
- Guarantees connectivity

### Why BFS for solving?

- Always finds shortest path
- Efficient

---

## 🔢 "42" Pattern

A fixed pattern is embedded in the center of the maze using fully closed cells.

- Ensures visibility in rendering
- An error message will be displayed if the maze is too small

## 📚 Resources

- DFS & BFS algorithms
- Graph theory (spanning trees)
- Python packaging documentation
- ANSI escape code

## 🤖 AI Usage

AI was used for:

- Understanding packaging requirements
- Structuring the README