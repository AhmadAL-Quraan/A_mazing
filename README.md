*This activity has been created as part of the 42 curriculum by Ahmad AL-Quraan and Alhareth Tahtamoni.*

## Description
This project aims to make a maze generator and solver. The output is a visual and playable board for a Pac-Man-like game.
A maze is generated as either **perfect** or **imperfect**:
* **Perfect maze**: Exactly one path between any two nodes, resulting in a lot of dead ends.
* **Imperfect maze**: At least two independent paths (loops) between any two nodes in the maze, ensuring a chased player always has an alternative route.

![](./pic/class_diagram.jpeg)
* Generated maze (perfect)
![](./pic/maze_example.png)

* Generated maze (imperfect)
![](./pic/maze_exampl_imperfect.png)

## Instructions
To run the main program:
```bash
python a_maze_ing.py config.txt
```

### Reusable Maze Generator (`mazegen`)
This project includes a reusable maze generation library that can be installed via `pip`.
The package is built as a `.whl` file (`mazegen-1.0.0-py3-none-any.whl`).

**Installation:**
```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

**Configuration example**:

```txt

WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42
```

**Usage Example:**
```python
from mazegen.generator import Generator
from mazegen.grid import Grid
from config import Config # Your custom configuration structure

# 1. Instantiate and pass custom parameters (e.g. size, seed)
config = Config(width=15, height=15, entry=(0,0), exit=(14,14), output_file="", perfect=False)
generator = Generator(config)

# 2. Access the generated structure
grid: Grid = generator.generate()
cell = grid.get_cell(0, 0)
print(f"Cell 0,0 walls -> N:{cell.north}, E:{cell.east}, S:{cell.south}, W:{cell.west}")

# 3. Access at least a solution (shortest path)
from solver import bfs_solve
shortest_path = bfs_solve(grid, config.entry, config.exit)
print("Shortest Path Coordinates:", shortest_path)
```

## Configuration File Format
The program relies on a configuration text file to generate the maze. The file must strictly follow the `KEY=VALUE` format, with one pair per line. Lines starting with `#` are treated as comments and ignored.
* `WIDTH`: Number of columns (integer > 0)
* `HEIGHT`: Number of rows (integer > 0)
* `ENTRY`: Starting coordinates in `x,y` format (e.g., `0,0`)
* `EXIT`: Ending coordinates in `x,y` format (e.g., `19,14`)
* `OUTPUT_FILE`: Name of the text file where the hexadecimal output is written (e.g., `maze.txt`)
* `PERFECT`: Boolean flag (`True` or `False`) to determine the generation mode.

## Algorithms
* **Perfect Generation**: DFS (Depth-First Search) with Backtracking.
* **Imperfect Generation**: Uses the perfect algorithm as a baseline, but loops through the maze afterward to break extra walls randomly (using a seed) on cells that only have 1 open wall (dead ends).
* **Pathfinding**: BFS (Breadth-First Search) to find the shortest path between the entry and exit cells.

### Why we chose these algorithms
* **DFS Backtracking** was chosen for maze generation because it is relatively simple to implement, fast, and creates long, winding corridors with high "river" characteristics (long, twisty paths), which are visually interesting and challenging.
* **BFS** was chosen for the solver because, unlike DFS, it mathematically guarantees finding the *shortest* path in an unweighted grid.

## Advanced Features
* **42 Logo Encoding**: The generator has custom logic to carve out a visible "42" pattern composed of fully closed cells in the center of the maze.
* **Interactive Visualization (`MazeView`)**: Provides options to re-generate the maze on the fly, toggle the visual shortest path overlay, and rotate the maze wall colors.

## Team and Project Management
* **Roles**: 
  * *Ahmad AL-Quraan*: Responsible for the core maze generation algorithms (DFS/Perfect/Imperfect), the shortest path solver (BFS), and the graphical rendering/visualization interface (`MazeView`).
  * *Alhareth Tahtamoni*: Responsible for configuration parsing, strict validation and error handling, the Hexadecimal file output writer (`Hexawriter`), Project Infrastructure (Makefile, README), and Python library packaging (`.whl`/`pyproject.toml`).
* **Planning and Evolution**: We initially divided the project cleanly between logic (generation) and infrastructure (I/O). The plan evolved smoothly, though we had to spend extra coordination time ensuring our data structures (`Grid`/`Cell`) were highly modular so the Hexawriter and MazeView could share the same data flawlessly.
* **What worked well**: Defining the `@dataclass` structures early on allowed us to work completely independently on our assigned modules without breaking each other's code.
* **What could be improved**: We could have set up standard linting (`flake8`/`mypy`) slightly earlier in the process to prevent a backlog of minor syntax/typing fixes right before the final build.
* **Tools Used**: Git/GitHub for version control and branching, Pytest (temporarily for logic testing), Flake8 for PEP8 linting, Mypy for strict static type checking, and the `build` module for `.whl` packaging.

## Resources
* [Wikipedia: Maze generation algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm) - Reference for DFS Backtracking logic.
* [Red Blob Games: Breadth First Search](https://www.redblobgames.com/pathfinding/a-star/introduction.html) - Pathfinding concepts.
* **AI Usage**: Artificial Intelligence was utilized as a coding assistant to enforce PEP257 styling, write strict static type annotations (`mypy`), build the `output_writer` bitwise logic, correctly format `pyproject.toml`. 

## Tasks 
- [x] Configuration file and format and error checking.
- [x] Perfect maze algorithm.
- [x] Imperfect maze algorithm.
- [x] Print and configure 42 Logo 
- [x] Makefile
- [x] Hexawriter
- [x] Shortest path between start and end.
- [x] Generating .whl file and pyproject.toml
- [x] README
- [x] Flake8 and mypy check 
- [x] Docstrings
- [x] Fixing Seed issue


## Debugging  

* Used `maze_analyzer.py` to check whether the generated maze is used by pacman or not.
* If perfect maze (not used by pacman):
![](./pic/perfect_maze.png)

* If Imperfect maze (used by pacman):
![](./pic/imperfect_maze.png)
