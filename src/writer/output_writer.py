from src.mazegen.grid import Grid
from src.mazegen.cell import Cell


def writer_hex(
    grid: Grid,
    shortest_path: list[tuple[int, int]],
    entry: tuple[int, int],
    exit: tuple[int, int],
    row: int,
    col: int,
    file_name: str,
) -> None:
    """Write the hexa data into the given file

    Args:
        grid: Takes the grid after generating the maze
        shortest_path: The list of the shortest path nodes between entry
           and exit
        entry: entry point
        exit: exit point
        row: Number of rows (height)
        col: Number of col (width)
        file_name: desired file to print to
    """
    try:
        with open(file_name, "w") as file:
            for x in range(row):
                for y in range(col):
                    cell: Cell = grid.get_cell(y, x)
                    cell_value: int = 0
                    if cell.north is True:
                        cell_value += 1
                    if cell.east is True:
                        cell_value += 2
                    if cell.south:
                        cell_value += 4
                    if cell.west:
                        cell_value += 8

                    file.write(str(hex(cell_value)[2:]))

                file.write("\n")

            file.write(f"\n{entry[0]},{entry[1]}\n")
            file.write(f"{exit[0]},{exit[1]}")
            shortest_path.reverse()
            directions: str = ""
            # print(shortest_path)
            for coordinate in range(1, len(shortest_path)):
                current = shortest_path[coordinate]
                before = shortest_path[coordinate - 1]
                if current[0] != before[0]:
                    if current[0] > before[0]:
                        directions += "E"
                    if current[0] < before[0]:
                        directions += "W"
                if current[1] != before[1]:
                    if current[1] > before[1]:
                        directions += "S"
                    if current[1] < before[1]:
                        directions += "N"
            # print(directions)
            file.write(f"\n{directions}")

    except Exception as e:
        print(f"Invalid file {e}")
