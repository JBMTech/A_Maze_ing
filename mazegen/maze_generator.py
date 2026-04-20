import random
from mazegen import constants
from collections import deque

# APLICARE EL ALGORITMO DFS PARA GENERAR EL CAMINO DEL LABERINTO
class MazeGenerator:
    def __init__(self, config: dict):
        self.width = config["WIDTH"]
        self.height = config["HEIGHT"]
        self.entry = config["ENTRY"]
        self.exit = config["EXIT"]
        self.perfect = config["PERFECT"]

        #random.seed(config["SEED"])

        self.grid = []
        
        self.solution_path = []
        self.wall_color = constants.BLUE
        self.pattern_42 = set()
    
    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    
    def open_path(self, x, y , direction):
        self.grid[y][x] &= ~direction

    def has_path(self, x, y, direction):
        return (self.grid[y][x] & direction) == 0

    def connect_cells(self, x, y, direction):
        nx = x + constants.DX[direction]
        ny = y + constants.DY[direction]

        if not self.in_bounds(nx, ny):
            return
    
        self.open_path(x, y, direction)
        self.open_path(nx, ny, constants.OPPOSITE[direction])

    def dfs(self, x, y):
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

    def generate(self):
        self.pattern_42.clear()
        self.grid = [[15 for _ in range(self.width)]
                     for _ in range(self.height)]
        self.solution_path = []
        start_x, start_y = self.entry
        self.apply_42_pattern()
        self.dfs(start_x, start_y)


    # PRINT ASCII
    def print_maze(self, show_path=False):
        print("+" + (self.wall_color + "---" + constants.RESET + "+") * self.width)

        for y in range(self.height):
            line_top = self.wall_color + "|" + constants.RESET
            line_bottom = "+"

            for x in range(self.width):
                if (x, y) == self.entry:
                    cell = " E "
                elif (x, y) == self.exit:
                    cell = " X "
                elif (x, y) in self.pattern_42:
                    cell = constants.YELLOW + "███" + constants.RESET
                elif show_path and (x, y) in self.solution_path:
                    cell = constants.GREEN + " o " + constants.RESET
                else:
                    cell = "   "

                # pared ESTE
                if self.has_path(x, y, constants.Direction.E):
                    line_top += cell + " "
                else:
                    line_top += cell + self.wall_color + "|" + constants.RESET

                # pared SUR
                if self.has_path(x, y, constants.Direction.S):
                    line_bottom += "   +"
                else:
                    line_bottom += self.wall_color + "---" + constants.RESET + "+"

            print(line_top)
            print(line_bottom)


    def apply_42_pattern(self):
        cx = self.width // 2
        cy = self.height // 2

        pattern = [
            (0,0),
            (0,1),
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
                self.grid[y][x] = 15
                self.pattern_42.add((x, y))


    # CAMBIAR COLOR
    def change_color(self):
        print("\n==== ELIGE TU COLOR ====")
        print("------------------------")
        print("1. Rojo")
        print("2. Verde")
        print("3. Azul")

        choice = input("Color: ")

        if choice == "1":
            self.wall_color = constants.RED
        elif choice == "2":
            self.wall_color = constants.GREEN
        elif choice == "3":
            self.wall_color = constants.BLUE

    def write_maze(self, filename):
        with open(filename, "w") as f:
            for y in range(self.height):
                line = ""
                for x in range(self.width):
                    value = self.grid[y][x]
                    line += hex(value)[2:].upper()
                f.write(line + "\n")

            f.write("\n")

            f.write(f"{self.entry[0]}, {self.entry[1]}\n")
            f.write(f"{self.exit[0]}, {self.exit[1]}\n")

            path = self.solve()
            f.write(path + "\n")


    def solve(self):
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

                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = (x, y)
                        queue.append((nx, ny))
        
        cur = self.exit

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

