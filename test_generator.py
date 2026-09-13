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


class FakeConfig:
    """Bare-bones stand-in for Config, just holding what Generator needs."""

    def __init__(
        self, width: int, height: int, seed: int | None, perfect: bool
    ) -> None:
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect


def main() -> None:
    config = FakeConfig(width=6, height=6, seed=42, perfect=True)

    generator = Generator(config)
    grid = generator.generate()

    entry = (0, 0)
    exit_ = (config.width - 1, config.height - 1)

    view = MazeView(grid, entry, exit_, bfs_stub, generator)
    view.run()


if __name__ == "__main__":
    main()
