import sys


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

        entry = config["ENTRY"].split(",")
        exit_ = config["EXIT"].split(",")

        config["ENTRY"] = (int(entry[0]), int(entry[1]))
        config["EXIT"] = (int(exit_[0]), int(exit_[1]))

        config["PERFECT"] = config["PERFECT"] == "True"

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

    print(config) # Debug

if __name__ == "__main__":
    main()
