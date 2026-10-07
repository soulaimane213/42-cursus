import sys
import os
import time
from typing import Optional, List, Tuple
from output_file import write_output
from parser import parser
from maze_generate import MazeGenerator

COLORS = [
    "\033[97m",  # white
    "\033[92m",  # green
    "\033[94m",  # blue
    "\033[93m",  # yellow
    "\033[91m",  # red
]
RESET = "\033[0m"
START_COLOR = "\033[94m"
END_COLOR = "\033[91m"
PATH_COLOR = "\033[92m"


def clear_screen() -> None:
    os.system("clear")


def print_maze(
    maze: MazeGenerator,
    show_solution: bool = False,
    color: str = "\033[97m",
    start: Optional['MazeGenerator.Cell'] = None,
    end: Optional['MazeGenerator.Cell'] = None,
) -> None:
    width = maze.width
    for _ in range(width):
        print(color + "◆═══", end="")
    print(color + "◆" + RESET)
    for row in maze.maze:
        for cell in row:
            left_wall = "║" if cell.left else " "
            if cell.blocked:
                content = "███"
            elif show_solution and cell.solution:
                if cell == start:
                    content = START_COLOR + " S " + RESET
                elif cell == end:
                    content = END_COLOR + " E " + RESET
                else:
                    content = PATH_COLOR + " ◉ " + RESET
            else:
                content = "   "
            print(color + f"{left_wall}{content}", end="")
        print(color + "║" + RESET)
        for cell in row:
            bottom_wall = "═══" if cell.down else "   "
            print(color + f"◆{bottom_wall}", end="")
        print(color + "◆" + RESET)


def animate_path(
    maze: MazeGenerator,
    path: List['MazeGenerator.Cell'],
    start: 'MazeGenerator.Cell',
    end: 'MazeGenerator.Cell',
    color: str,
) -> None:
    for row in maze.maze:
        for cell in row:
            cell.solution = False
    for cell in path:
        cell.solution = True
        clear_screen()
        print_maze(maze, True, color, start, end)
        print(f"\n🧭 Path length: {len(path)} cells")
        time.sleep(0.05)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return
    try:
        config = parser(sys.argv[1])
    except Exception as e:
        print(e)
        return
    for required in ("WIDTH", "HEIGHT", "ENTRY", "EXIT", "PERFECT",
                     "OUTPUT_FILE"):
        if required not in config:
            print(f"Error: Missing required config key: {required}")
            return
    width: int = config["WIDTH"]
    height: int = config["HEIGHT"]
    entry_coords: Tuple[int, int] = config["ENTRY"]
    exit_coords: Tuple[int, int] = config["EXIT"]
    entry_col, entry_row = entry_coords
    exit_col, exit_row = exit_coords
    seed: Optional[int] = None
    file_name = config["OUTPUT_FILE"]

    try:
        seed = config["SEED"]
    except Exception:
        pass

    generation_time: float = 0

    def build_new_maze(var: Optional[int]) -> MazeGenerator:
        nonlocal generation_time
        start_time = time.time()
        m = MazeGenerator(width, height)
        if width >= 10 and height >= 10:
            m.draw_42()
        if config["PERFECT"]:
            m.add_extra_paths((entry_row, entry_col), (exit_row, exit_col))
        m.remove_walls(var)
        end_time = time.time()
        generation_time = end_time - start_time
        return m

    def solve_maze(m: MazeGenerator) -> List['MazeGenerator.Cell']:
        start = m.maze[entry_row][entry_col]
        end = m.maze[exit_row][exit_col]
        if start.blocked or end.blocked:
            print("Error: Invalid ENTRY/EXIT position (blocked cell)")
            sys.exit(1)
        return m.bfs(start, end)

    maze = build_new_maze(seed)
    path = solve_maze(maze)
    sta = (entry_row, entry_col)
    ends = (exit_row, exit_col)
    write_output(maze, path, sta, ends, file_name)
    show_solution = False
    color_index = 0
    try:
        while True:
            clear_screen()
            start = maze.maze[entry_row][entry_col]
            end = maze.maze[exit_row][exit_col]
            print_maze(maze, show_solution, COLORS[color_index], start, end)
            if show_solution and path:
                print(f"\n🧭 Path length: {len(path)} cells")
            print(f"\n⏱️ Generation time: {generation_time:.4f} seconds")
            print("\n=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path (animated)")
            print("3. Rotate colors")
            print("4. Quit")
            choice = input("Choice? (1-4): ").strip()
            if choice == "1":
                maze = build_new_maze(var=None)
                path = solve_maze(maze)
                sta = (entry_row, entry_col)
                ends = (exit_row, exit_col)
                write_output(maze, path, sta, ends, file_name)
                show_solution = False
            elif choice == "2":
                if not show_solution:
                    animate_path(
                        maze,
                        path,
                        start,
                        end,
                        COLORS[color_index]
                    )
                    show_solution = True
                else:
                    for row in maze.maze:
                        for cell in row:
                            cell.solution = False
                    show_solution = False
            elif choice == "3":
                color_index = (color_index + 1) % len(COLORS)
            elif choice == "4":
                print("Bye 👋")
                break
            else:
                print("Invalid choice!")
    except (KeyboardInterrupt, EOFError):
        print("\n\n[!] Program interrupted (Ctrl+C). Bye 👋")
    write_output(maze, path, sta, ends, file_name)


if __name__ == "__main__":
    main()
