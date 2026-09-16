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
        print(config.seed)

    def patternn(self, patterN_42: set[tuple[int, int]]) -> None:
        """Draw the 42 pattern on the grid

        closed wall => True
        Open wall => false

        Args:
           patterN_42: Spot 42 pattern in the grid and reference it

        """
        width = self.config.width
        height = self.config.height
        if width >= 9 and height >= 7:
            x: int = int((width - 7) / 2)
            y: int = int((height - 5) / 2)
            patterN_42.add((x, y))
            y += 1
            patterN_42.add((x, y))
            y += 1
            patterN_42.add((x, y))
            x += 1
            patterN_42.add((x, y))
            x += 1
            patterN_42.add((x, y))
            y += 1
            patterN_42.add((x, y))
            y += 1
            patterN_42.add((x, y))
            x += 2
            y -= 4
            patterN_42.add((x, y))
            x += 1
            patterN_42.add((x, y))
            x += 1
            patterN_42.add((x, y))
            y += 1
            patterN_42.add((x, y))
            y += 1
            patterN_42.add((x, y))
            x -= 1
            patterN_42.add((x, y))
            x -= 1
            patterN_42.add((x, y))
            y += 1
            patterN_42.add((x, y))
            y += 1
            patterN_42.add((x, y))
            x += 1
            patterN_42.add((x, y))
            x += 1
            patterN_42.add((x, y))

    def generate(self) -> Grid:
        """Generate and return a maze as a Grid.

        Returns:
            A fully carved Grid, perfect if config.perfect is True.
        """
        grid: Grid = Grid(self.config.width, self.config.height)
        dx = [1, -1, 0, 0]
        dy = [0, 0, 1, -1]
        directions = ["east", "west", "south", "north"]

        visited: set[tuple[int, int]] = set()
        patterN_42: set[tuple[int, int]] = set()
        self.patternn(patterN_42)
        for x, y in patterN_42:
            cell = grid.get_cell(x, y)
            cell.east = True
            cell.north = True
            cell.south = True
            cell.west = True

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
                    and (new_x, new_y) not in patterN_42
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

        if not self.config.perfect:
            for y in range(self.config.height):
                for x in range(self.config.width):
                    if (x, y) in patterN_42:
                        continue
                    not_broken: list[str] = []
                    cell = grid.get_cell(x, y)
                    count: int = 4
                    if cell.east is True:
                        count -= 1
                        if x != self.config.width - 1:
                            not_broken.append("east")
                    if cell.north is True:
                        count -= 1
                        if y != 0:
                            not_broken.append("north")
                    if cell.south is True:
                        count -= 1
                        if y != self.config.height - 1:
                            not_broken.append("south")
                    if cell.west is True:
                        count -= 1
                        if x != 0:
                            not_broken.append("west")

                    choose: str
                    if count == 1:

                        choose = self.rng.choice(not_broken)
                        if choose == "east" and (x + 1, y) not in patterN_42:
                            cell.east = False
                            grid.get_cell(x + 1, y).west = False
                        if choose == "west" and (x - 1, y) not in patterN_42:
                            cell.west = False
                            grid.get_cell(x - 1, y).east = False
                        if choose == "north" and (x, y - 1) not in patterN_42:
                            cell.north = False

                            grid.get_cell(x, y - 1).south = False
                        if choose == "south" and (x, y + 1) not in patterN_42:
                            cell.south = False
                            grid.get_cell(x, y + 1).north = False

        return grid
