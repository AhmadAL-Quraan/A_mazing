from .mazegen.grid import Grid
from collections import deque
from .mazegen.cell import Cell


def bfs_solve(
    grid: Grid, entry: tuple[int, int], exit: tuple[int, int]
) -> list[tuple[int, int]]:
    """Bfs algorithm to find the shortest path between entry and exit

    Args:
        Grid: The grid :)
        entry: Starting point
        exit: Ending point


    """
    queue: deque[tuple[int, int]] = deque()
    queue.append(entry)
    visited: set[tuple[int, int]] = set()
    cost: dict[tuple[int, int], int] = {}
    parent: dict[tuple[int, int], tuple[int, int]] = {}
    parent[entry] = entry
    visited.add(entry)
    cost[entry] = 0
    while queue:
        x, y = queue.popleft()
        cell: Cell = grid.get_cell(x, y)
        if not cell.east and (x + 1, y) not in visited:
            queue.append((x + 1, y))
            parent[(x + 1, y)] = (x, y)
            cost[(x + 1, y)] = cost[(x, y)] + 1
            visited.add((x + 1, y))
        if not cell.west and (x - 1, y) not in visited:
            queue.append((x - 1, y))
            parent[(x - 1, y)] = (x, y)
            cost[(x - 1, y)] = cost[(x, y)] + 1
            visited.add((x - 1, y))
        if not cell.north and (x, y - 1) not in visited:
            queue.append((x, y - 1))
            parent[(x, y - 1)] = (x, y)
            cost[(x, y - 1)] = cost[(x, y)] + 1
            visited.add((x, y - 1))
        if not cell.south and (x, y + 1) not in visited:
            queue.append((x, y + 1))
            parent[(x, y + 1)] = (x, y)
            cost[(x, y + 1)] = cost[(x, y)] + 1
            visited.add((x, y + 1))

    answer: list[tuple[int, int]] = []
    start, end = exit
    while parent[(start, end)] != (start, end):
        answer.append((start, end))
        start, end = parent[(start, end)]

    answer.append(entry)
    return answer
