from typing import Dict, Any, Tuple


def parser(file_name: str) -> Dict[str, Any]:
    config: Dict[str, Any] = dict()

    try:
        with open(file_name, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line[0] == '#':
                    continue
                content = line.split("=")
                if len(content) != 2:
                    raise ValueError(f"Error: Invalid config line: {line}")

                key = content[0].strip().upper()
                value = content[1].strip()

                if key == "WIDTH":
                    if key in config:
                        raise ValueError(
                            f"Error: Duplicate configuration key: {key}")
                    if not value.isdigit() or int(value) < 5 or \
                            int(value) >= 50:
                        raise ValueError(f"Invalid value for {key}")
                    config[key] = int(value)

                elif key == "HEIGHT":
                    if key in config:
                        raise ValueError(
                            f"Error: Duplicate configuration key: {key}")
                    if not value.isdigit() or int(value) < 5 or \
                            int(value) >= 50:
                        raise ValueError(f"Invalid value for {key}")
                    config[key] = int(value)

                elif key in ("ENTRY", "EXIT"):
                    if key in config:
                        raise ValueError(
                            f"Error: Duplicate configuration key: {key}")
                    x_and_y = value.split(",")
                    if len(x_and_y) != 2:
                        raise ValueError(f"Invalid value for {key}")
                    x, y = x_and_y[0].strip(), x_and_y[1].strip()
                    if not x.isdigit() or not y.isdigit():
                        raise ValueError(f"Invalid value for {key}")
                    config[key] = (int(x), int(y))

                elif key == "OUTPUT_FILE":
                    if key in config:
                        raise ValueError(
                            f"Error: Duplicate configuration key: {key}")
                    if not value.endswith(".txt"):
                        raise ValueError(
                            f"Invalid value for {key}: must end \
                                with '.txt', got '{value}'")
                    if value.startswith("."):
                        raise ValueError(
                            f"Invalid value for {key}: must not \
                                start with '.', got '{value}'")
                    config[key] = value

                elif key == "PERFECT":
                    if key in config:
                        raise ValueError(
                            f"Error: Duplicate configuration key: {key}")
                    config[key] = value

                elif key == "SEED":
                    if key in config:
                        raise ValueError(
                            f"Error: Duplicate configuration key: {key}")
                    try:
                        config[key] = int(value)
                    except ValueError:
                        raise ValueError(
                            f"Invalid value for SEED: must be an integer,"
                            f" got '{value}'")

        # Validate ENTRY/EXIT bounds after full file is parsed
        for key in ("ENTRY", "EXIT"):
            if key in config:
                coords: Tuple[int, int] = config[key]
                cx, cy = coords
                if cx < 0 or cy < 0 or cx >= config["WIDTH"] or \
                        cy >= config["HEIGHT"]:
                    raise ValueError(f"Invalid value for {key}")

    except FileNotFoundError:
        print(f"Error: Configuration file '{file_name}' not found")
        exit(1)
    if config["EXIT"] == config["ENTRY"]:
        print("exit and entry can't be in the same point")
        exit(1)

    return config
