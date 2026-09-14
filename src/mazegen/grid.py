from dataclasses import dataclass, field
from .cell import Cell


@dataclass
class Grid:
    """A 2D grid of maze cells.

    Stores the maze as a row-major list of lists, where each cell tracks
    its own walls. Cells are automatically created and populated based on
    the given width and height when the Grid is instantiated.

    Attributes:
        width: Number of columns in the grid.
        height: Number of rows in the grid.
        cells: Row-major 2D list of Cell objects, indexed as
            cells[y][x]. Auto-populated in __post_init__ if not
            explicitly provided.
    """

    width: int
    height: int
    cells: list[list[Cell]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.cells:
            self.cells = [
                [Cell(x, y) for x in range(self.width)]
                for y in range(self.height)
            ]

    def get_cell(self, x: int, y: int) -> Cell:
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError(f"({x},{y}) out of bounds")
        return self.cells[y][x]

    def print_cells(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                print(f"({self.cells[y][x].x}, {self.cells[y][x].y})")
