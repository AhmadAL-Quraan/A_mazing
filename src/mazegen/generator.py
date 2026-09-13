from .grid import Grid
from src.config import Config
import random


class Generator:
    """Generates a maze using a randomized recursive backtracker."""

    def __init__(self, config: Config) -> None:
        """Initialize the generator with a parsed configuration.

        Args:
            config: Parsed maze configuration (width, height, seed, etc).
        """
        self.config = config
        self.rng = random.Random(config.seed)

    def generate(self) -> Grid:
        """Generate and return a maze as a Grid.

        Returns:
            A fully carved Grid, perfect if config.perfect is True.
        """
        grid: Grid = Grid(self.config.width, self.config.height)
        dx = [1, -1, 0, 0]
        dy = [0, 0, 1, -1]
        directions = ["east", "west", "south", "north"]

        if self.config.perfect:
            visited: set[tuple[int, int]] = set()
            stack: list[tuple[int, int]] = [(0, 0)]
            visited.add((0, 0))

            while stack:
                x, y = stack[-1]
                neighbors: list[tuple[int, int, str]] = []
                for i in range(4):
                    new_x = x + dx[i]
                    new_y = y + dy[i]
                    if (
                        (new_x, new_y) not in visited
                        and 0 <= new_x < self.config.width
                        and 0 <= new_y < self.config.height
                    ):
                        neighbors.append((new_x, new_y, directions[i]))

                if not neighbors:
                    stack.pop()
                    continue

                nx, ny, direction = self.rng.choice(neighbors)
                current = grid.get_cell(x, y)
                neighbor = grid.get_cell(nx, ny)

                if direction == "east":
                    current.east = False
                    neighbor.west = False
                elif direction == "south":
                    current.south = False
                    neighbor.north = False
                elif direction == "west":
                    current.west = False
                    neighbor.east = False
                elif direction == "north":
                    current.north = False
                    neighbor.south = False

                visited.add((nx, ny))
                stack.append((nx, ny))

        return grid
