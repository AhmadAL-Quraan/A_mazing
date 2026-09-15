from src.mazegen.grid import Grid
import sys


class OutputWriter:
    @staticmethod
    def write(
        grid: Grid,
        entry: tuple[int, int],
        exit_coord: tuple[int, int],
        path: list[tuple[int, int]],
        filepath: str,
    ) -> None:
        """Writes the maze configuration and solution to a file."""
        if not path:
            path_str = ""
        else:
            ordered = path[::-1]
            if ordered[0] != entry:
                ordered = path

            directions = []
            for i in range(len(ordered) - 1):
                curr = ordered[i]
                nxt = ordered[i + 1]
                if nxt[0] == curr[0] + 1 and nxt[1] == curr[1]:
                    directions.append("E")
                elif nxt[0] == curr[0] - 1 and nxt[1] == curr[1]:
                    directions.append("W")
                elif nxt[0] == curr[0] and nxt[1] == curr[1] + 1:
                    directions.append("S")
                elif nxt[0] == curr[0] and nxt[1] == curr[1] - 1:
                    directions.append("N")
            path_str = "".join(directions)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                for y in range(grid.height):
                    row_hex = ""
                    for x in range(grid.width):
                        cell = grid.get_cell(x, y)
                        val = 0
                        if cell.north:
                            val |= 1
                        if cell.east:
                            val |= 2
                        if cell.south:
                            val |= 4
                        if cell.west:
                            val |= 8
                        row_hex += hex(val)[2:].upper()
                    f.write(row_hex + "\n")

                f.write("\n")
                f.write(f"{entry[0]},{entry[1]}\n")
                f.write(f"{exit_coord[0]},{exit_coord[1]}\n")
                f.write(path_str + "\n")
        except OSError as e:
            print(f"Error writing output to {filepath}: {e}", file=sys.stderr)

