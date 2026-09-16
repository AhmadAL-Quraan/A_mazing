# Overview

* This project aims to make a maze for pacman-like game.
 
 A maze is either a **perfect** or **Imperfect** :
* Perfect maze: one path between any two nodes, with a lot of dead ends in the maze.
* Imperfect maze: At least two paths between any two nodes in the maze with least dead ends.


![](./pic/class_diagram.jpeg)

# Algorithms

* **Perfect**: DFS with backtracking to make the perfect maze.
* **Imperfect**: uses the perfect algorithm but break extra walls by checking which cells has 1 open wall and break another one randomly using seed.
* **BFS algorithm** to find shortest path between entry and exit cells as requested in the task.


# Tasks 


- [x] Configuration file and format and error checking.
- [x] Perfect maze algorithm.
- [x] Imperfect maze algorithm.
- [x] Print and configure 42 Logo 
- [x] Makefile
- [ ] Hexawriter
- [x] Shortest path between start and end.
- [ ] Generating .whl file and pyproject.toml
- [x] README
- [ ] Check mypy and flake8
- [ ] Docstrings

