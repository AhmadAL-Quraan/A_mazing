"""Quick manual test: run the perfect-maze Generator and view it live.

Run from the project root with:
    python3 -m test_generator

This bypasses Config entirely -- Generator is built directly with plain
values, so you can test it without Solver, Config, or the CLI being
finished yet.
"""

from src.mazegen.generator import Generator
from src.maze_view.maze_view import MazeView
from stub_solver import bfs_stub

from src.config import Config


def main() -> None:
    config = Config(10,10,(0,0),(9,9),"output_file.txt",False,42)
    generator = Generator(config)
    grid = generator.generate()

    entry = (0, 0)
    exit_ = (config.width - 1, config.height - 1)

    view = MazeView(grid, entry, exit_, bfs_stub, generator)
    view.run()


if __name__ == "__main__":
    main()
