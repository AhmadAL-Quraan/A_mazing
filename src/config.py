from dataclasses import dataclass
from pathlib import Path


class ConfigError(Exception):
    """Raised when the configuration contains invalid data."""


@dataclass
class Config:
    """Store validated maze configuration.

    Attributes:
        width: Number of columns in the maze.
        height: Number of rows in the maze.
        entry: (x, y) coordinate of the maze entrance.
        exit: (x, y) coordinate of the maze exit.
        output_file: Path to the file the maze output will be written to.
        perfect: Whether the maze should be generated as a perfect maze
            (no loops).
        seed: Optional random seed for reproducible generation.
    """

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None


def parse_config(filepath: str) -> Config:
    """Read, parse, and validate a configuration file.

    Reads a KEY=VALUE formatted file, converts each required field to its
    proper type, and validates the resulting configuration.

    Args:
        filepath: Path to the configuration file.

    Returns:
        A validated Config instance.

    Raises:
        ConfigError: If the file cannot be found or read, contains
            malformed lines, is missing required keys, has duplicate
            keys, or fails validation.
    """
    path = Path(filepath)

    try:
        with path.open("r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError as exc:
        raise ConfigError(
            f"Configuration file '{filepath}' was not found."
        ) from exc
    except OSError as exc:
        raise ConfigError(
            f"Could not read configuration file '{filepath}': {exc}"
        ) from exc

    data: dict[str, str] = {}

    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            raise ConfigError(f"Line {line_number}: expected KEY=VALUE.")

        key, value = line.split("=", 1)
        key = key.strip().upper()
        value = value.strip()

        if not key:
            raise ConfigError(
                f"Line {line_number}: configuration key is empty."
            )

        # SEED is allowed to be empty (SEED= with nothing after it);
        # every other key still requires a non-empty value.
        if not value and key != "SEED":
            raise ConfigError(
                f"Line {line_number}: value for '{key}' is empty."
            )

        if key in data:
            raise ConfigError(f"Line {line_number}: duplicate key '{key}'.")

        data[key] = value

    required_keys = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    }

    missing = required_keys - data.keys()

    if missing:
        raise ConfigError(
            "Missing required key(s): " + ", ".join(sorted(missing))
        )

    width = parse_positive_int(data["WIDTH"], "WIDTH")
    height = parse_positive_int(data["HEIGHT"], "HEIGHT")
    entry = parse_coordinate(data["ENTRY"], "ENTRY")
    exit_coord = parse_coordinate(data["EXIT"], "EXIT")
    perfect = parse_bool(data["PERFECT"], "PERFECT")
    seed = parse_optional_seed(data.get("SEED"))

    config = Config(
        width=width,
        height=height,
        entry=entry,
        exit=exit_coord,
        output_file=data["OUTPUT_FILE"],
        perfect=perfect,
        seed=seed,
    )

    validate_config(config)

    return config


def parse_int(value: str, key: str) -> int:
    """Convert a configuration value to an integer.

    Args:
        value: The raw string value to convert.
        key: Name of the configuration key, used in error messages.

    Returns:
        The parsed integer.

    Raises:
        ConfigError: If value cannot be converted to an integer.
    """
    try:
        return int(value)
    except ValueError as exc:
        raise ConfigError(f"{key} must be an integer, got '{value}'.") from exc


def parse_positive_int(value: str, key: str) -> int:
    """Convert a configuration value to a positive integer.

    Args:
        value: The raw string value to convert.
        key: Name of the configuration key, used in error messages.

    Returns:
        The parsed integer, guaranteed to be greater than 0.

    Raises:
        ConfigError: If value is not an integer, or is not greater than 0.
    """
    number = parse_int(value, key)

    if number <= 0:
        raise ConfigError(f"{key} must be greater than 0, got {number}.")

    return number


def parse_coordinate(value: str, key: str) -> tuple[int, int]:
    """Parse coordinates in x,y format.

    Args:
        value: The raw string value, expected as "x,y".
        key: Name of the configuration key, used in error messages.

    Returns:
        A tuple of (x, y) integers.

    Raises:
        ConfigError: If value is not in "x,y" format, or x/y are not
            valid integers.
    """
    parts = value.split(",")

    if len(parts) != 2:
        raise ConfigError(f"{key} must use x,y format, got '{value}'.")

    x = parse_int(parts[0].strip(), key)
    y = parse_int(parts[1].strip(), key)

    return x, y


def parse_bool(value: str, key: str) -> bool:
    """Convert True/False text to a boolean.

    Args:
        value: The raw string value, expected to be "True" or "False"
            (case-insensitive).
        key: Name of the configuration key, used in error messages.

    Returns:
        The parsed boolean.

    Raises:
        ConfigError: If value is not "True" or "False".
    """
    normalized = value.lower()

    if normalized == "true":
        return True

    if normalized == "false":
        return False

    raise ConfigError(f"{key} must be True or False, got '{value}'.")


def parse_optional_seed(value: str | None) -> int | None:
    """Parse the optional SEED value.

    Args:
        value: The raw SEED value from the config file, or None if the
            SEED key was never present at all.

    Returns:
        The parsed integer seed, or None if the key was absent or its
        value was left empty (e.g. "SEED=" with nothing after it).

    Raises:
        ConfigError: If a non-empty SEED value is present but is not a
            valid integer.
    """
    if value is None or value == "":
        return None

    return parse_int(value, "SEED")


def validate_config(config: Config) -> None:
    """Validate the configuration values.

    Checks that the entry and exit coordinates fall within the maze
    bounds and that they are not the same cell.

    Args:
        config: The Config instance to validate.

    Raises:
        ConfigError: If entry or exit is outside the maze bounds, or if
            entry and exit are the same coordinate.
    """
    entry_x, entry_y = config.entry
    exit_x, exit_y = config.exit

    if not (0 <= entry_x < config.width and 0 <= entry_y < config.height):
        raise ConfigError(
            f"ENTRY {config.entry} is outside maze bounds "
            f"{config.width}x{config.height}."
        )

    if not (0 <= exit_x < config.width and 0 <= exit_y < config.height):
        raise ConfigError(
            f"EXIT {config.exit} is outside maze bounds "
            f"{config.width}x{config.height}."
        )

    if config.entry == config.exit:
        raise ConfigError("ENTRY and EXIT must be different.")
