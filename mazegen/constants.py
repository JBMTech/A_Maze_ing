from enum import IntEnum


class Direction(IntEnum):
    N = 1  # bit 0
    E = 2  # bit 1
    S = 4  # bit 2
    W = 8  # bit 3


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
