import sys
from mazegen.maze_generator import MazeGenerator


def parse_config(file_name: str) -> dict:
    """
    Retrieves the maze information from a file.

    Arguments:
        file_name (str): The name of the file.

    Returns:
        dict: The maze configuration.
    """
    config: dict = {}

    try:
        with open(file_name, "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ValueError("Invalid config line")

                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()

    except FileNotFoundError:
        print("Error: file not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    return config


def validate_keys(config: dict) -> None:
    """
    Validates the required maze configuration parameters.

    Args:
        config (dict): The maze configuration.

    """
    required_keys = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT"
    ]

    for key in required_keys:
        if key not in config:
            print(f"Error: missing key {key}")
            sys.exit(1)


def convert_config(config: dict) -> dict:
    """
    Validates and converts configuration values.

    Args:
        config (dict): Maze configuration.

    Returns:
        dict: Valid values for generating the maze.
    """
    try:
        config["WIDTH"] = int(config["WIDTH"])
        config["HEIGHT"] = int(config["HEIGHT"])

        if ((config["WIDTH"] <= 0 or config["HEIGHT"] <= 0)):
            print("Error: invalid maze size")
            sys.exit(1)

        entry = config["ENTRY"].split(",")
        exit_ = config["EXIT"].split(",")

        if len(entry) != 2 or len(exit_) != 2:
            print("Error: invalid ENTRY or EXIT format")
            sys.exit(1)

        config["ENTRY"] = (int(entry[0]), int(entry[1]))
        config["EXIT"] = (int(exit_[0]), int(exit_[1]))

        x, y = config["ENTRY"]
        if x < 0 or x >= config["WIDTH"] or y < 0 or y >= config["HEIGHT"]:
            print("Error: ENTRY out of bounds")
            sys.exit(1)

        if config["ENTRY"] == config["EXIT"]:
            print("Error: ENTRY and EXIT cannot be the same")
            sys.exit(1)

        x, y = config["EXIT"]
        if x < 0 or x >= config["WIDTH"] or y < 0 or y >= config["HEIGHT"]:
            print("Error: EXIT out of bounds")
            sys.exit(1)

        if config["PERFECT"] == "True":
            config["PERFECT"] = config["PERFECT"]
        elif config["PERFECT"] == "False":
            config["PERFECT"] = config["PERFECT"]
        else:
            print("Error: invalid PERFECT")
            sys.exit(1)

        if "SEED" in config:
            config["SEED"] = int(config["SEED"])
        else:
            config["SEED"] = None

    except Exception:
        print("Error: invalid config values")
        sys.exit(1)

    return config


def main() -> None:
    """
    Main entry point of the application.

    Displays the interactive menu and handles user actions.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    file_name = sys.argv[1]

    config = parse_config(file_name)
    validate_keys(config)
    config = convert_config(config)

    maze = MazeGenerator(config)
    show_path_toggle: bool = False

    while True:
        print("\033[?25h", end="")
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Animate maze generation (BONUS)")
        print("5. Quit")

        choice = input("Choice? (1-5): ").strip()

        if choice == "1":
            print("\033[2J\033[H", end="")
            show_path_toggle = False
            maze.generate(False)
            maze.print_maze(show_path_toggle)

        elif choice == "2":
            try:
                print("\033[2J\033[H", end="")
                show_path_toggle = not show_path_toggle
                if show_path_toggle and not maze.solution_path:
                    maze.solve()
                    maze.write_maze(config["OUTPUT_FILE"])
                maze.print_maze(show_path_toggle)
            except Exception:
                print("\n[Error]: Maze not solved")

        elif choice == "3":
            if maze.grid:
                print("\033[2J\033[H", end="")
                maze.change_color()
                maze.print_maze(show_path_toggle)
            else:
                print("\n[Error]: Maze not generated")

        elif choice == "4":
            print("\033[2J\033[H", end="")
            show_path_toggle = False
            maze.generate(True)

        elif choice == "5":
            print("Bye!")
            break

        else:
            print("\033[2J\033[H", end="")
            print("\n[Error]: Invalid option.")


if __name__ == "__main__":
    main()
