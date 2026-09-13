import sys

from src.config import ConfigError, parse_config


def main() -> None:
    """Run A-Maze-ing."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>", file=sys.stderr)
        sys.exit(1)

    try:
        config = parse_config(sys.argv[1])
    except ConfigError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    print(config)

    # Later:
    # generator = Generator(config)
    # grid = generator.generate()


if __name__ == "__main__":
    main()
