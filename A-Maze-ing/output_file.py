from typing import List, Tuple
from maze_generate import MazeGenerator


def write_output(
    maze: MazeGenerator,
    path: List['MazeGenerator.Cell'],
    entry: Tuple[int, int],
    exit_: Tuple[int, int],
    filepath: str,
) -> None:

    directions: List[str] = []
    for i in range(len(path) - 1):
        curr = path[i]
        nxt = path[i + 1]
        if nxt.row < curr.row:
            directions.append("N")
        elif nxt.row > curr.row:
            directions.append("S")
        elif nxt.col > curr.col:
            directions.append("E")
        else:
            directions.append("W")

    with open(filepath, "w") as f:
        for row in maze.maze:
            line = ""
            for cell in row:
                val = 0
                if cell.top:
                    val |= 1
                if cell.right:
                    val |= 2
                if cell.down:
                    val |= 4
                if cell.left:
                    val |= 8
                line += format(val, 'X')
            f.write(line + "\n")

        f.write("\n")
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit_[0]},{exit_[1]}\n")
        f.write("".join(directions) + "\n")
