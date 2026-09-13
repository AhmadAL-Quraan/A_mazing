from dataclasses import dataclass
from pathlib import Path


class ConfigError(Exception):
    """Raised when the configuration contains invalid data."""


@dataclass
class Config:
    """Store validated maze configuration."""

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool


def parse_config(filepath: str) -> Config:
    """Read, parse, and validate a configuration file."""
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

        if not value:
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

    config = Config(
        width=width,
        height=height,
        entry=entry,
        exit=exit_coord,
        output_file=data["OUTPUT_FILE"],
        perfect=perfect,
    )

    validate_config(config)

    return config


def parse_int(value: str, key: str) -> int:
    """Convert a configuration value to an integer."""
    try:
        return int(value)
    except ValueError as exc:
        raise ConfigError(f"{key} must be an integer, got '{value}'.") from exc


def parse_positive_int(value: str, key: str) -> int:
    """Convert a configuration value to a positive integer."""
    number = parse_int(value, key)

    if number <= 0:
        raise ConfigError(f"{key} must be greater than 0, got {number}.")

    return number


def parse_coordinate(
    value: str,
    key: str,
) -> tuple[int, int]:
    """Parse coordinates in x,y format."""
    parts = value.split(",")

    if len(parts) != 2:
        raise ConfigError(f"{key} must use x,y format, got '{value}'.")

    x = parse_int(parts[0].strip(), key)
    y = parse_int(parts[1].strip(), key)

    return x, y


def parse_bool(value: str, key: str) -> bool:
    """Convert True/False text to a boolean."""
    normalized = value.lower()

    if normalized == "true":
        return True

    if normalized == "false":
        return False

    raise ConfigError(f"{key} must be True or False, got '{value}'.")


def validate_config(config: Config) -> None:
    """Validate the configuration values."""
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
