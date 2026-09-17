import sys
from src.config import ConfigError, parse_config
from src.mazegen.generator import Generator
from src.maze_view.maze_view import MazeView
from src.solver import bfs_solve
from src.writer.output_writer import writer_hex


def main() -> None:
    """Parse configuration file,
      generate a maze then write the output (hexadecimal format)

    Reads a config file path form command line arg, parses
    it then draw the maze

    Raises:
         SystemExit: If the number of command line is incorrect or the config
         file is wrong misconfigured
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>", file=sys.stderr)
        sys.exit(1)

    try:
        config = parse_config(sys.argv[1])
    except ConfigError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    generator = Generator(config)
    grid, check_error = generator.generate()
    if check_error == 1:
        sys.exit(1)

    shortest = bfs_solve(grid, config.entry, config.exit)
    view = MazeView(grid, config.entry, config.exit, bfs_solve, generator)
    view.run()
    writer_hex(
        grid,
        shortest,
        config.entry,
        config.exit,
        config.height,
        config.width,
        config.output_file,
    )


if __name__ == "__main__":
    main()
