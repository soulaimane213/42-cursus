*This project has been created as part of the 42 curriculum by \<ilaaouin\>, \<sofadl\>.*

# A-Maze-ing: Maze Generator

## Description
A-Maze-ing is a Python project that generates random mazes, optionally perfect (with a single path between entry and exit), and allows visual display in the terminal. This project explores maze generation algorithms, randomness, and pathfinding while producing a reusable Python package (`mazegen-*`) for future projects.

The maze generation logic is implemented in a standalone module (`MazeGenerator`) and can be imported, configured, and used independently from the main program.

## Instructions

### Installation & Usage
Use the provided Makefile to run and manage the project:

- **Install dependencies**:
```bash
make install
Run the main program:

make run
Run in debug mode:

make debug
Clean temporary files:

make clean
Lint and type-check code:

make lint
Optional strict linting:

make lint-strict
Example Config (config.txt):
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
Using the Reusable Module:
from mazegen.generator import MazeGenerator

# Create a maze generator with custom size and seed
maze_gen = MazeGenerator(width=15, height=15, seed=42)

# Access the maze structure
maze = maze_gen.get_maze()
for row in maze:
    print("".join([' ' if cell == 0 else '#' for cell in row]))

# Access a solution (naive shortest path)
solution = maze_gen.get_solution()
print("Solution path:", solution)
Configuration File Format
WIDTH and HEIGHT: Maze dimensions (integer number of cells)

ENTRY and EXIT: Coordinates of the entrance and exit (x,y)

OUTPUT_FILE: Filename for hexadecimal maze output

PERFECT: Boolean (True or False) to indicate if maze is perfect

SEED: Optional integer for reproducible randomnesime: 0.0002 secondss

Lines starting with # are ignored (comments)

Maze Generation Algorithm
The project uses the Depth-First Search (DFS) recursive backtracker algorithm:

Each cell starts with walls on all four sides.

DFS randomly visits unvisited neighbors, carving passages.

Backtracking occurs when no unvisited neighbors remain.

If PERFECT=True, the resulting maze has exactly one path between entry and exit.

Why DFS?
Simple to implement and understand.

Naturally produces a perfect maze.

Supports reproducible results using a random seed.

Reusable Code
The maze generation logic is encapsulated in the MazeGenerator class:

Accepts parameters: width, height, and optional seed.

Provides access to the generated maze structure.

Provides a method to retrieve at least one solution path.

Fully independent of input parsing and visualization logic.

Team and Project Management
ilaaouin: Maze generation logic, algorithm implementation, solution path calculation.

sofadl: Parsing configuration, visual display, terminal rendering, and packaging as a Python module.

Reflections
DFS algorithm worked well for perfect mazes; random seed ensured reproducibility.

Visualization helped debug maze connectivity and solution paths.

Packaging the module as a single-file reusable library simplified reuse for future projects.

Resources
DFS algorithm concept: Wikipedia DFS

Maze generation techniques: Red Blob Games – Maze Generation

AI was used to:

Explain DFS and BFS concepts.

Search for maze generation algorithms and pathfinding strategies.

Assist in structuring the reusable module for pip installation.