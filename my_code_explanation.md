# Code Explanation: My Parts of the Project

This document is a deep dive into the logic behind the code I wrote. It explains exactly *how* my parts of the code work under the hood, which is useful for defending the project.

---

## 1. Configuration Parsing (`src/config.py`)

My goal was to read a text file (like `config.txt`), extract its settings, and strictly enforce the rules so the rest of the program never has to deal with bad data.

### How the parsing loop works:
Inside `parse_config(filepath: str)`:
1. **Reading the file:** I open the file safely using a `with` block. If the file doesn't exist, it throws a `FileNotFoundError`, which I catch and convert into a custom `ConfigError` to exit gracefully.
2. **Line-by-line processing:** I use `enumerate(lines, start=1)` so that if an error happens, I can tell the user exactly which line number caused it.
3. **Ignoring junk:** `line.strip()` removes hidden whitespace/newlines. If the line is empty or starts with `#`, I use `continue` to skip it.
4. **Extracting Key/Value:** I check for an equals sign (`=`). If it's there, I use `line.split("=", 1)`. The `1` is crucial: it means "only split on the *first* equals sign". This ensures that if a filename is `my=maze.txt`, it doesn't break the code.
5. **Deduplication:** I check if the key already exists in my `data` dictionary. If it does, I throw an error to prevent duplicate settings.

### Type Conversion & Validation:
Once I have the raw strings in the dictionary, I need to convert them to Python types:
* **`parse_positive_int`:** Tries to convert the string to an integer. If the string is a letter (e.g., "A"), Python throws a `ValueError`. I catch it and return a friendly `ConfigError`. Then I check `if number <= 0` because a maze cannot have a negative size.
* **`parse_coordinate`:** Splits the string by `,`. It passes the left side (X) and right side (Y) to the integer parser and returns them as a tuple: `(x, y)`.

Finally, `validate_config` checks the logic. It ensures the `entry` and `exit` coordinates are not the same, and verifies that `entry_x < config.width` (meaning the start point isn't placed completely outside the maze boundaries). I use a `@dataclass` (`Config`) to neatly package all these validated variables together.

---

## 2. The Hexawriter (`src/writer/output_writer.py`)

My task here was to take our in-memory grid of cells and translate it into a specific hexadecimal text format, as well as calculate the directional path (N, E, S, W).

### Bitwise Wall Encoding (The Hexadecimal logic)
The subject requires closing walls to be represented by bits: North=1, East=2, South=4, West=8.
Inside `OutputWriter.write`:
1. I loop through every `y` (row) and `x` (column).
2. For each cell, I start with a value of `0` (`val = 0`).
3. I use the **Bitwise OR operator (`|=`)**:
   * If `cell.north` is closed (True), `val |= 1`.
   * If `cell.south` is closed (True), `val |= 4`.
   * *Example:* If a cell has North and South closed, `0 | 1 | 4 = 5`. 
4. **Hex Conversion:** I use Python's built-in `hex(val)`. `hex(10)` returns `"0xa"`. I use slicing `[2:]` to chop off the `"0x"`, leaving just `"a"`, and then `.upper()` to make it `"A"`. I append this character to the row string.

### Path Translation
The BFS solver returns a list of coordinate tuples (e.g., `[(0,0), (0,1), (1,1)]`). I had to turn this into a string of letters.
1. I loop through the list, looking at the `curr` (current) coordinate and the `nxt` (next) coordinate.
2. I do simple math:
   * If `nxt[0] == curr[0] + 1`: The X coordinate increased, so we moved **East** (`E`).
   * If `nxt[1] == curr[1] + 1`: The Y coordinate increased, so we moved **South** (`S`).
3. I append these letters to a list, join them into a single string, and write it at the very bottom of the file under the coordinates.

---

## 3. Package Generation (`pyproject.toml` & `.whl`)

The subject required the maze generator to be reusable as a Python library.

* **`pyproject.toml`**: This file acts as the blueprint for the package. Instead of old `setup.py` scripts, modern Python uses this TOML file to define the project's metadata (Name: `mazegen`, Version: `1.0.0`, dependencies). It tells the build system to look inside the `src` folder for the `mazegen` code.
* **Building**: I used the `build` module (`python -m build`). This reads the `pyproject.toml` blueprint and compresses the code into a `.whl` (Wheel) file. A Wheel is a pre-compiled ZIP archive that makes it incredibly fast and easy for someone else to `pip install` our code in a completely different project without having to re-compile anything.

---

## 4. Automation (`Makefile`)

To make the project easy to evaluate and compile, I wrote a POSIX-compliant Makefile. 
* **`make lint`**: Runs `flake8` to check for PEP8 styling errors (like missing spaces or lines being too long) and runs `mypy --strict` to ensure every single function has perfect type hints (like `tuple[int, int]`).
* **`make clean`**: I used `rm -rf` to delete hidden cache folders like `__pycache__` and `.mypy_cache`. These are temporary folders Python generates to speed up execution, but they clutter the project. Cleaning them ensures the evaluator gets a fresh run.

