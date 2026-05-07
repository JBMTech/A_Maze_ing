import sys
from mazegen.maze_generator import MazeGenerator


def parse_config(file_name: str) -> dict:
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

        config["PERFECT"] = config["PERFECT"] == "True"

        if "SEED" in config:
            config["SEED"] = int(config["SEED"])
        else:
            config["SEED"] = None

    except Exception:
        print("Error: invalid config values")
        sys.exit(1)

    return config


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    file_name = sys.argv[1]

    config = parse_config(file_name)
    validate_keys(config)
    config = convert_config(config)

    # Test para visualizar laberinto en ASCII
    maze = MazeGenerator(config)

    while True:
        print("\n===== A_MAZE_ING =======")
        print("------------------------")
        print("1. Generar laberinto")
        print("2. Mostrar solución")
        print("3. Ocultar solución")
        print("4. Cambiar color")
        print("5. Salir")

        choice = input("Opción: ")

        if choice == "1":
            maze.generate()
            maze.print_maze()

        elif choice == "2":
            try:
                if not maze.solution_path:
                    maze.solve()
                    maze.write_maze(config["OUTPUT_FILE"])
                maze.print_maze(show_path=True)
            except Exception:
                print("\n[Error]: laberinto no resuelto")

        elif choice == "3":
            if maze.solution_path:
                maze.print_maze(show_path=False)

        elif choice == "4":
            maze.change_color()

        elif choice == "5":
            break


if __name__ == "__main__":
    main()
