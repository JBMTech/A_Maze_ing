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

class MazeGenerator:
    def __init__(self, config: dict):
        self.width = config["WIDTH"]
        self.height = config["HEIGHT"]
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]
        self.perfect = config["PERFECT"]
        self.grid = [[0 for _ in range(self.width)]
                     for _ in range(self.height)]
    
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
    
        self.grid[y][x] |= direction
        self.grid[ny][nx] |= OPPOSITE[direction]

    def dfs(self, x, y):
        directions = list(Direction)
        random.shuffle(directions)

        for d in directions:
            nx = x + DX[d]
            ny = y + DY[d]

            if self.in_bounds(nx, ny) and self.grid[ny][nx] == 0:
                self.connect_cells(x, y, d)
                self.dfs(nx, ny)

    def generator(self):
        start_x, start_y = self.entry
        self.dfs(start_x, start_y)

    def print_maze(self):
    # línea superior
        print("+" + "---+" * self.width)

        for y in range(self.height):
            line_top = "|"
            line_bottom = "+"

            for x in range(self.width):
                # contenido celda
                if (x, y) == self.entry:
                    cell = " E "
                elif (x, y) == self.exit:
                    cell = " X "
                else:
                    cell = "   "

                # pared Este
                if self.has_path(x, y, Direction.E):
                    line_top += cell + " "
                else:
                    line_top += cell + "|"

                # pared Sur
                if self.has_path(x, y, Direction.S):
                    line_bottom += "   +"
                else:
                    line_bottom += "---+"

            print(line_top)
            print(line_bottom)
    
