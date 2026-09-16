"""Terminal ASCII rendering and interactive controls for a generated maze.

Provides the MazeView class, which draws a Grid using box-drawing style
ASCII art, highlights the entry/exit cells and the "42" pattern, can
show/hide the shortest solution path, cycle through wall colors (via
ANSI escape codes), and re-generate a fresh maze on demand -- all
through a simple numbered terminal menu.
"""

from __future__ import annotations

import os
from typing import Callable

from src.mazegen.cell import Cell
from src.mazegen.generator import Generator
from src.mazegen.grid import Grid

# ANSI color codes used to "recolor" the maze walls between refreshes.
_WALL_COLORS: list[str] = [
    "\033[97m",  # white
    "\033[93m",  # yellow
    "\033[96m",  # cyan
    "\033[92m",  # green
    "\033[95m",  # magenta
]
_RESET = "\033[0m"
_ENTRY_COLOR = "\033[95m"  # magenta block
_EXIT_COLOR = "\033[91m"  # red block
_PATTERN_COLOR = "\033[90m"  # dim gray block for the "42" pattern
_PATH_COLOR = "\033[96m"  # cyan for the solution path


class MazeView:
    """Renders a Grid to the terminal and drives the interactive menu.

    Attributes:
        grid: The Grid currently being displayed.
        entry: (x, y) coordinates of the maze entrance.
        exit: (x, y) coordinates of the maze exit.
        show_path: Whether the shortest path should currently be drawn.
        path: Cached list of (x, y) coordinates for the shortest path,
            or an empty list if not yet computed.
        color_index: Index into _WALL_COLORS for the current wall color.
    """

    def __init__(
        self,
        grid: Grid,
        entry: tuple[int, int],
        exit: tuple[int, int],
        solver_fn: Callable[
            [Grid, tuple[int, int], tuple[int, int]], list[tuple[int, int]]
        ],
        generator: Generator,
    ) -> None:
        """Initialize the view.

        Args:
            grid: The maze grid to display.
            entry: Entry coordinates (x, y).
            exit: Exit coordinates (x, y).
            solver_fn: Callable that returns a list of (x, y) coordinates
                forming the shortest path from entry to exit.
            generator: The MazeGenerator used to produce new mazes when
                the user chooses to regenerate.
        """
        self.grid = grid
        self.entry = entry
        self.exit = exit
        self._solver_fn = solver_fn
        self._generator = generator
        self.show_path = False
        self.path: list[tuple[int, int]] = []
        self.color_index = 0

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def draw(self) -> None:
        """Render the current grid to the terminal.

        Draws walls as box-drawing characters, highlights the entry and
        exit cells, shades the "42" pattern cells, and overlays the
        solution path if show_path is enabled.
        """
        os.system("cls" if os.name == "nt" else "clear")
        wall_color = _WALL_COLORS[self.color_index]
        path_cells = set(self.path) if self.show_path else set()

        lines = self._build_ascii_grid(wall_color, path_cells)
        print("\n".join(lines))

    def _build_ascii_grid(
        self, wall_color: str, path_cells: set[tuple[int, int]]
    ) -> list[str]:
        """Build the list of printable lines representing the maze.

        Args:
            wall_color: ANSI color code to use for wall characters.
            path_cells: Set of (x, y) coordinates on the solution path,
                empty if the path should not be highlighted.

        Returns:
            A list of strings, one per terminal row, ready to print.
        """
        width, height = self.grid.width, self.grid.height
        lines: list[str] = []

        # Top border
        top = (
            wall_color
            + "+"
            + "+".join("--" for _ in range(width))
            + "+"
            + _RESET
        )
        lines.append(top)

        for y in range(height):
            row_mid = wall_color + "|" + _RESET
            row_bottom = wall_color + "+" + _RESET

            for x in range(width):
                cell = self.grid.get_cell(x, y)
                row_mid += self._render_cell_body(
                    cell, x, y, path_cells, wall_color
                )
                row_mid += self._render_wall(cell.east, wall_color)
                row_bottom += self._render_wall(
                    cell.south, wall_color, horizontal=True
                )
                row_bottom += wall_color + "+" + _RESET

            lines.append(row_mid)
            lines.append(row_bottom)

        return lines

    def _render_cell_body(
        self,
        cell: Cell,
        x: int,
        y: int,
        path_cells: set[tuple[int, int]],
        wall_color: str,
    ) -> str:
        """Return the two-character interior representation of one cell."""
        if (x, y) == self.entry:
            return f"{_ENTRY_COLOR}##{_RESET}"
        if (x, y) == self.exit:
            return f"{_EXIT_COLOR}##{_RESET}"
        if self._is_pattern_cell(cell):
            return f"{_PATTERN_COLOR}##{_RESET}"
        if (x, y) in path_cells:
            return f"{_PATH_COLOR}..{_RESET}"
        return "  "

    @staticmethod
    def _render_wall(
        closed: bool, color: str, horizontal: bool = False
    ) -> str:
        """Return the character(s) representing one wall segment.

        Args:
            closed: Whether this wall is closed (should be drawn).
            color: ANSI color code to wrap the wall character in.
            horizontal: True for a top/bottom wall segment (two chars
                wide, to match the cell body width), False for a
                left/right wall segment (one char wide).
        """
        if horizontal:
            return f"{color}--{_RESET}" if closed else "  "
        return f"{color}|{_RESET}" if closed else " "

    @staticmethod
    def _is_pattern_cell(cell: Cell) -> bool:
        """Return True if a cell is part of the sealed '42' pattern.

        A pattern cell is fully closed on all four sides and is not
        reachable from the rest of the maze by construction.
        """
        return cell.north and cell.east and cell.south and cell.west

    # ------------------------------------------------------------------
    # Interactive menu
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Run the interactive terminal menu loop until the user quits."""
        self.draw()
        while True:
            print()
            print("=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")
            choice = input("Choice? (1-4): ").strip()

            if choice == "1":
                self._regenerate()
            elif choice == "2":
                self._toggle_path()
            elif choice == "3":
                self._rotate_color()
            elif choice == "4":
                break
            else:
                print("Invalid choice, please enter 1-4.")
                continue

            self.draw()

    def _regenerate(self) -> None:
        """Generate a brand new maze and reset path/display state."""
        self.grid = self._generator.generate()[0]
        self.path = []
        self.show_path = False

    def _toggle_path(self) -> None:
        """Toggle display of the shortest entry-to-exit path.

        Computes and caches the path the first time it is requested.
        """
        if not self.path:
            self.path = self._solver_fn(self.grid, self.entry, self.exit)
        self.show_path = not self.show_path

    def _rotate_color(self) -> None:
        """Cycle to the next wall color."""
        self.color_index = (self.color_index + 1) % len(_WALL_COLORS)
