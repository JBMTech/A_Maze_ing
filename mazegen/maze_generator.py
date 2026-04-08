from enum import IntEnum
import random

# APLICARE EL ALGORITMO DFS PARA GENERAR EL CAMINO DEL LABERINTO
class Direction(IntEnum):
    N = 1
    S = 2
    E = 4
    W = 8


DX = {Direction.E: 1,
      Direction.W: -1,
      Direction.N: 0,
      Direction.S: 0}

DY = {Direction.E: 0,
      Direction.W: 0,
      Direction.N: -1,
      Direction.S: 1}

OPPOSITE = {Direction.E: Direction.W,
            Direction.W: Direction.E,
            Direction.N: Direction.S,
            Direction.S: Direction.N}

# COLORES
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RESET = "\033[0m"


class MazeGenerator:
    def __init__(self, config: dict):
        self.width = config["WIDTH"]
        self.height = config["HEIGHT"]
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]
        self.perfect = config["PERFECT"]

        #random.seed(config["SEED"])

        self.grid = [[0 for _ in range(self.width)]
                     for _ in range(self.height)]
        
        self.solution_path = []
        self.wall_color = RED
        self.pattern_42 = set()
    
    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    
    def open_path(self, x, y , direction):
        self.grid[y][x] |= direction

    def has_path(self, x, y, direction):
        return (self.grid[y][x] & direction) != 0

    def connect_cells(self, x, y, direction):
        nx = x + DX[direction]
        ny = y + DY[direction]

        if not self.in_bounds(nx, ny):
            return
    
        self.open_path(x, y, direction)
        self.open_path(nx, ny, OPPOSITE[direction])

    def dfs(self, x, y):
        directions = list(Direction)
        random.shuffle(directions)

        for d in directions:
            nx = x + DX[d]
            ny = y + DY[d]

            if self.in_bounds(nx, ny) and self.grid[ny][nx] == 0:
                self.connect_cells(x, y, d)
                self.dfs(nx, ny)

    def generate(self):
        start_x, start_y = self.entry
        self.dfs(start_x, start_y)
        self.apply_42_pattern()


    # PRINT ASCII
    def print_maze(self, show_path=False):
        print("+" + (self.wall_color + "---" + RESET + "+") * self.width)

        for y in range(self.height):
            line_top = self.wall_color + "|" + RESET
            line_bottom = "+"

            for x in range(self.width):
                if (x, y) == self.entry:
                    cell = " E "
                elif (x, y) == self.exit:
                    cell = " X "
                elif (x, y) in self.pattern_42:
                    cell = YELLOW + "███" + RESET
                elif show_path and (x, y) in self.solution_path:
                    cell = " * "
                else:
                    cell = "   "

                # pared ESTE
                if self.has_path(x, y, Direction.E):
                    line_top += cell + " "
                else:
                    line_top += cell + self.wall_color + "|" + RESET

                # pared SUR
                if self.has_path(x, y, Direction.S):
                    line_bottom += "   +"
                else:
                    line_bottom += self.wall_color + "---" + RESET + "+"

            print(line_top)
            print(line_bottom)


    def apply_42_pattern(self):
        cx = self.width // 2
        cy = self.height // 2

        pattern = [
            (0,0),(2,0),
            (0,1),(2,1),
            (0,2),(1,2),(2,2),
            (2,3),(2,4),

            (4,0),(5,0),(6,0),
            (6,1),
            (4,2),(5,2),(6,2),
            (4,3),
            (4,4),(5,4),(6,4)
        ]

        self.pattern_42.clear()

        for dx, dy in pattern:
            x = cx + dx - 3
            y = cy + dy - 2

            if self.in_bounds(x, y):
                self.grid[y][x] = 0
                self.pattern_42.add((x, y))


    # CAMBIAR COLOR
    def change_color(self):
        print("\n=== ELIGE TU COLOR ===")
        print("------------------------")
        print("1. Rojo")
        print("2. Verde")
        print("3. Azul")

        choice = input("Color: ")

        if choice == "1":
            self.wall_color = RED
        elif choice == "2":
            self.wall_color = GREEN
        elif choice == "3":
            self.wall_color = BLUE
    
