import random
import sys
from typing import Any
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

        self.seed = config["SEED"]

        if self.seed is not None:
            random.seed(self.seed)

        self.grid = []

        self.solution_path = []
        self.wall_color = constants.BLUE
        self.pattern_42 = set()

    # Comprueba si una celda esta dentro del laberinto
    def in_bounds(self, x, y) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def open_path(self, x, y, direction) -> None:
        '''
        Permite abrir un camino eliminando una pared.
            ~direction:
            invierte los bits de la dirección para crear una máscara.
        Ejemplo:
            EAST = 0100
            ~EAST = 1011

        &= aplica la máscara sobre la celda.
        El bit de la dirección se convierte en 0,
        eliminando esa pared.
        '''
        self.grid[y][x] &= ~direction

    # Comprueba si la pared existe en esa direccion
    def has_path(self, x, y, direction) -> bool:
        """
        Comprueba si existe un camino abierto
        en una dirección específica.

        Usa una operación AND bit a bit para verificar
        si el bit de la dirección sigue activo.

        Si el resultado es 0:
        - no hay pared
        - existe un camino
        """
        return (self.grid[y][x] & direction) == 0

    # conecta esta celda con su vecina en esa direccion
    def connect_cells(self, x, y, direction) -> None:
        """
        Conecta dos celdas vecinas eliminando
        las paredes correspondientes.

        Abre la pared de la celda actual en la
        dirección indicada y también abre la
        pared opuesta en la celda vecina,
        garantizando una conexión bidireccional.
        """
        nx = x + constants.DX[direction]
        ny = y + constants.DY[direction]

        if not self.in_bounds(nx, ny):
            return

        self.open_path(x, y, direction)
        self.open_path(nx, ny, constants.OPPOSITE[direction])

    def dfs(self, x, y) -> None:
        '''
        1. Mezcla direcciones aleatoriamente
        2. Intenta avanzar
        3. Si el vecino es válido y no visitado:
            - rompe la pared
            - entra recursivamente
        4. Repite hasta llenar todo el laberinto
        '''
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
        self.pattern_42.clear()
        self.grid = [[15 for _ in range(self.width)]
                     for _ in range(self.height)]

        if self.width < 7 or self.height < 5:
            print("Error: maze too small for 42 pattern")
            sys.exit(1)

        self.solution_path = []
        start_x, start_y = self.entry
        self.apply_42_pattern()
        self.dfs(start_x, start_y)

        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 15 and (x, y) not in self.pattern_42:
                    self.dfs(x, y)

        if not self.perfect:
            self.add_loops()

    # PRINT ASCII
    def print_maze(self, show_path=False) -> None:
        print("+" + (self.wall_color + "---" + constants.RESET + "+")
              * self.width)

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

    def apply_42_pattern(self) -> None:
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

    # CAMBIAR COLOR
    def change_color(self) -> None:
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

    def write_maze(self, filename) -> None:
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

    def solve(self) -> Any:
        '''
        Resuelve el laberinto utilizando BFS (Breadth-First Search).

        BFS explora el laberinto por niveles utilizando una cola (FIFO),
        garantizando encontrar el camino más corto entre la entrada y la salida.

        Funcionamiento general:
        1. Se comienza desde la entrada del laberinto.
        2. Se exploran todas las celdas vecinas accesibles.
        3. Cada celda visitada se guarda en `visited`
        para evitar repetir posiciones.
        4. El diccionario `parent` almacena desde qué celda
        se llegó a otra, permitiendo reconstruir el camino final.
        5. Cuando se alcanza la salida, se reconstruye el camino
        retrocediendo desde la salida hasta la entrada usando `parent`.
        6. Finalmente, el camino se transforma en direcciones:
        N, S, E, W.
        '''
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

    def add_loops(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                for d in constants.Direction:
                    nx = x + constants.DX[d]
                    ny = y + constants.DY[d]

                    if self.in_bounds(nx, ny):
                        if random.random() < 0.1:
                            self.connect_cells(x, y, d)
