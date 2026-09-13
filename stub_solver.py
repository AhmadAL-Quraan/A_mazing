"""Temporary stand-in Solver, only for testing MazeView + Generator
in isolation before the real Solver is implemented.
"""

from src.mazegen.grid import Grid


def bfs_stub(
    grid: Grid, start: tuple[int, int], end: tuple[int, int]
) -> list[tuple[int, int]]:
    """Return an empty path -- just enough to satisfy MazeView's interface.

    Replace with the real Solver.bfs once it exists. This lets you test
    the generator + view without waiting on the Solver to be finished.
    """
    return []
