from enum import IntEnum


class Direction(IntEnum):
    N = 1
    E = 2
    S = 4
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

PURPLE = "\033[95m"
CYAN = "\033[96m"
DARKCYAN = "\033[36m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
