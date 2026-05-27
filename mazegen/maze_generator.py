import random
import sys
from typing import Any
from mazegen import constants
from collections import deque


class MazeGenerator:
    """
    A maze generator and solver based on DFS and BFS.

    The class allows you to:
    - generate perfect or imperfect mazes
    - connect cells by removing walls
    - print the maze to the console
    - export it to a file

    The maze is represented as a grid of integers
    where each bit indicates the presence of a wall.
    """
    def __init__(self, config: dict):
        self.width = config["WIDTH"]
        self.height = config["HEIGHT"]
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]
        self.perfect = config["PERFECT"]

        self.seed = None

        if config.get("SEED"):
            self.seed = config["SEED"]
            random.seed(self.seed)

        self.grid: list[Any] = []

        self.solution_path: list[Any] = []
        self.color_palette = [
            constants.BLUE,
            constants.PURPLE,
            constants.GREEN,
            constants.CYAN,
            constants.YELLOW,
            constants.RED,
            constants.DARKCYAN,
        ]
        self.current_color_idx = 0
        self.wall_color = self.color_palette[self.current_color_idx]
        self.pattern_42: set[Any] = set()

    def in_bounds(self, x: int, y: int) -> bool:
        """
        Check whether coordinates are inside maze bounds.

        Args:
            x (int): X coordinate.
            y (int): Y coordinate.

        Returns:
            bool: True if coordinates are valid, otherwise False.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    def open_path(self, x: int, y: int, direction: int) -> None:
        """
        Remove the wall in the given direction from a cell.

        Args:
            x (int): Cell X coordinate.
            y (int): Cell Y coordinate.
            direction (int): Wall direction bitmask.
        """
        self.grid[y][x] &= ~direction

    def has_path(self, x: int, y: int, direction: int) -> bool:
        """
        Check whether a path exists in the given direction.

        A bitwise AND operation is used to determine whether
        the wall bit is still active.

        Returns:
            bool: True if the wall is open, otherwise False.
        """
        if (self.grid[y][x] & direction) == 0:
            return True
        return False

    def connect_cells(self,
                      x: int,
                      y: int,
                      direction: constants.Direction) -> None:
        """
        Connect two adjacent cells by removing the corresponding walls,
        ensuring a bidirectional connection.

        Args:
            x (int): Cell X coordinate.
            y (int): Cell Y coordinate.
            direction (constants.Direction): Wall direction bitmask.
        """
        nx = x + constants.DX[direction]
        ny = y + constants.DY[direction]

        if not self.in_bounds(nx, ny):
            return

        self.open_path(x, y, direction)
        self.open_path(nx, ny, constants.OPPOSITE[direction])

    def dfs(self, x: int, y: int) -> None:
        """
        Generate maze paths recursively using Depth-First Search (DFS).

        The algorithm visits random neighboring cells and removes
        walls to create a connected maze structure.

        Args:
            x (int): Cell X coordinate.
            y (int): Cell Y coordinate.
        """
        directions = list(constants.Direction)
        random.shuffle(directions)

        for d in directions:
            nx = x + constants.DX[d]
            ny = y + constants.DY[d]

            if (self.in_bounds(nx, ny)
                    and self.grid[ny][nx] == 15
                    and (nx, ny) not in self.pattern_42):
                self.connect_cells(x, y, d)
                self.dfs(nx, ny)

    def generate(self) -> None:
        """
        Generate the maze structure.

        Initializes the grid, applies the 42 pattern restriction,
        generates paths using DFS, and optionally adds loops
        for imperfect mazes.
        """
        self.pattern_42.clear()
        self.grid = [[15 for _ in range(self.width)]
                     for _ in range(self.height)]

        if self.width < 7 or self.height < 5:
            print("Error: maze too small for 42 pattern")
            sys.exit(1)

        self.solution_path = []
        start_x, start_y = self.entry

        self.apply_42_pattern()

        if self.entry in self.pattern_42:
            sys.exit("Error: ENTRY coordinates cannot be"
                     "inside the '42' pattern.")

        if self.exit in self.pattern_42:
            sys.exit("Error: EXIT coordinates cannot be"
                     "inside the '42' pattern.")

        self.dfs(start_x, start_y)

        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 15 and (x, y) not in self.pattern_42:
                    self.dfs(x, y)

        if self.perfect == "False":
            self.add_loops()

    def add_loops(self) -> None:
        """
        Randomly remove additional walls to create multiple paths.
        """
        for y in range(self.height):
            for x in range(self.width):
                if ((x, y) in self.pattern_42):
                    continue
                for d in constants.Direction:
                    nx = x + constants.DX[d]
                    ny = y + constants.DY[d]

                    if self.in_bounds(nx, ny):
                        if (nx, ny) in self.pattern_42:
                            continue
                        if random.random() < 0.1:
                            self.connect_cells(x, y, d)

    def print_maze(self, show_path: bool) -> None:
        """
        Print the maze to the terminal.

        Args:
            show_path (bool): Whether to display the solution path.
        """
        top_border = (self.wall_color + "█" + ("████" * self.width) +
                      constants.RESET)
        print(top_border)

        for y in range(self.height):
            line_top = self.wall_color + "█" + constants.RESET
            line_bottom = self.wall_color + "█" + constants.RESET

            for x in range(self.width):
                if (x, y) == self.entry:
                    cell = constants.PURPLE + " E " + constants.RESET
                elif (x, y) == self.exit:
                    cell = constants.RED + " X " + constants.RESET
                elif (x, y) in self.pattern_42:
                    cell = constants.YELLOW + "███" + constants.RESET
                elif show_path and (x, y) in self.solution_path:
                    cell = constants.GREEN + " ● " + constants.RESET
                else:
                    cell = "   "

                if self.has_path(x, y, constants.Direction.E):
                    line_top += cell + " "
                else:
                    line_top += cell + self.wall_color + "█" + constants.RESET

                if self.has_path(x, y, constants.Direction.S):
                    line_bottom += ("   " + self.wall_color + "█" +
                                    constants.RESET)
                else:
                    line_bottom += self.wall_color + "████" + constants.RESET

            print(line_top)
            print(line_bottom)

    def apply_42_pattern(self) -> None:
        """
        Reserve cells forming the '42' pattern in the maze center.

        Reserved cells are excluded from maze generation paths.
        """
        cx = self.width // 2
        cy = self.height // 2

        pattern = [
            (0, 0),
            (0, 1),
            (0, 2), (1, 2), (2, 2),
            (2, 3), (2, 4),

            (4, 0), (5, 0), (6, 0),
            (6, 1),
            (4, 2), (5, 2), (6, 2),
            (4, 3),
            (4, 4), (5, 4), (6, 4)
        ]

        self.pattern_42.clear()

        for dx, dy in pattern:
            x = cx + dx - 3
            y = cy + dy - 2

            if self.in_bounds(x, y):
                self.grid[y][x] = 15
                self.pattern_42.add((x, y))

    def change_color(self) -> None:
        """
        Cycle through available wall colors.
        """
        self.current_color_idx = ((self.current_color_idx + 1) %
                                  len(self.color_palette))
        self.wall_color = self.color_palette[self.current_color_idx]

    def solve(self) -> str:
        """
        Solve the maze using Breadth-First Search (BFS).

        BFS guarantees the shortest path between the maze
        entry and exit.

        Returns:
            str: Sequence of directions using N, S, E, and W.
        """
        self.solution_path = []
        queue = deque([self.entry])
        visited = set([self.entry])
        parent = {}

        while queue:
            x, y = queue.popleft()

            if (x, y) == self.exit:
                break

            for d in constants.Direction:
                if self.has_path(x, y, d):
                    nx = x + constants.DX[d]
                    ny = y + constants.DY[d]

                    if self.in_bounds(nx, ny) and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = (x, y)
                        queue.append((nx, ny))

        cur = self.exit

        if self.exit not in parent:
            raise Exception("No path found")

        while cur != self.entry:
            self.solution_path.append(cur)
            cur = parent[cur]

        self.solution_path.append(self.entry)
        self.solution_path.reverse()

        path_directions = []

        for i in range(1, len(self.solution_path)):
            x1, y1 = self.solution_path[i - 1]
            x2, y2 = self.solution_path[i]

            dx = x2 - x1
            dy = y2 - y1

            if dx == 1:
                path_directions.append("E")
            elif dx == -1:
                path_directions.append("W")
            elif dy == 1:
                path_directions.append("S")
            elif dy == -1:
                path_directions.append("N")

        return "".join(path_directions)

    def write_maze(self, filename: str) -> None:
        """
        Export the maze and solution path to a file.

        Args:
            filename (str): Output file path.
        """
        with open(filename, "w") as f:
            for y in range(self.height):
                line = ""
                for x in range(self.width):
                    value = self.grid[y][x]
                    line += hex(value)[2:].upper()
                f.write(line + "\n")

            f.write("\n")

            f.write(f"{self.entry[0]},{self.entry[1]}\n")
            f.write(f"{self.exit[0]},{self.exit[1]}\n")

            self.solution_path = []
            path = self.solve()
            f.write(path + "\n")
