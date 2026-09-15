import sys

from src.config import ConfigError, parse_config
from src.mazegen.generator import Generator
from src.maze_view.maze_view import MazeView
from src.solver import bfs_solve


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

    generator = Generator(config)
    grid = generator.generate()
    bfs_solve(grid, config.entry, config.exit)
    view = MazeView(grid, config.entry, config.exit, bfs_solve, generator)
    view.run()


if __name__ == "__main__":
    main()
