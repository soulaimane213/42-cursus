import random
from collections import deque
from typing import List, Tuple, Optional, Dict, Set, Deque


class MazeGenerator:
    """Maze generator with DFS-based maze creation, BFS pathfinding, and
    extra features."""

    class Cell:
        """Represents a single cell in the maze."""

        def __init__(self, row: int, col: int):
            self.row: int = row
            self.col: int = col
            self.top: bool = True
            self.right: bool = True
            self.down: bool = True
            self.left: bool = True
            self.blocked: bool = False
            self.visited: bool = False
            self.solution: bool = False
            self.start: bool = False
            self.end: bool = False

    def __init__(self, width: int, height: int):
        """Initialize maze with given width and height."""
        self.width: int = width
        self.height: int = height
        self.maze: List[List['MazeGenerator.Cell']] = self.mazeGen()

    def mazeGen(self) -> List[List['MazeGenerator.Cell']]:
        """Create empty maze grid with cells."""
        return [
            [self.Cell(r, c) for c in range(self.width)]
            for r in range(self.height)
        ]

    def draw_42(self) -> None:
        """Draw the '42' blocked pattern in the center of the maze."""
        center_row = self.height // 2
        center_col = self.width // 2
        start_row = center_row - 3
        start_col = center_col - 3
        for i in range(3):
            self.maze[start_row + i][start_col].blocked = True
        for i in range(3):
            self.maze[start_row + 2][start_col + i].blocked = True
        for j in range(3):
            self.maze[start_row + 2 + j][start_col + 2].blocked = True
        start_col += 4
        for j in range(3):
            self.maze[start_row][start_col + j].blocked = True
        for j in range(3):
            self.maze[start_row + j][start_col + 2].blocked = True
        for j in range(3):
            self.maze[start_row + 2][start_col + j].blocked = True
        for j in range(3):
            self.maze[start_row + 4][start_col + j].blocked = True
        for j in range(3):
            self.maze[start_row + 2 + j][start_col].blocked = True

    def where_to_go(
            self,
            cell: 'MazeGenerator.Cell') -> List['MazeGenerator.Cell']:
        """Return neighboring cells that are not blocked."""
        neighbors: List['MazeGenerator.Cell'] = []
        row, col = cell.row, cell.col
        if row > 0 and not self.maze[row - 1][col].blocked:
            neighbors.append(self.maze[row - 1][col])
        if row < self.height - 1 and not self.maze[row + 1][col].blocked:
            neighbors.append(self.maze[row + 1][col])
        if col > 0 and not self.maze[row][col - 1].blocked:
            neighbors.append(self.maze[row][col - 1])
        if col < self.width - 1 and not self.maze[row][col + 1].blocked:
            neighbors.append(self.maze[row][col + 1])
        return neighbors

    def remove_walls(self, Seed: Optional[int] = None) -> None:
        """Generate maze paths by removing walls using DFS."""
        if Seed is not None:
            random.seed(Seed)
        start_cell: 'MazeGenerator.Cell' = self.maze[0][0]
        start_cell.visited = True
        stack: List['MazeGenerator.Cell'] = [start_cell]
        while stack:
            current: 'MazeGenerator.Cell' = stack[-1]
            neighbors = self.where_to_go(current)
            unvisited = [c for c in neighbors if not c.visited]
            if unvisited:
                nxt: 'MazeGenerator.Cell' = random.choice(unvisited)
                if nxt.row < current.row:
                    current.top = False
                    nxt.down = False
                elif nxt.row > current.row:
                    current.down = False
                    nxt.top = False
                elif nxt.col < current.col:
                    current.left = False
                    nxt.right = False
                elif nxt.col > current.col:
                    current.right = False
                    nxt.left = False
                nxt.visited = True
                stack.append(nxt)
            else:
                stack.pop()

    def get_open_neighbors(
            self,
            cell: 'MazeGenerator.Cell') -> List['MazeGenerator.Cell']:
        """Return neighboring cells that can be moved to (no walls)."""
        neighbors: List['MazeGenerator.Cell'] = []
        row, col = cell.row, cell.col
        if row > 0 and not cell.top and not self.maze[row - 1][col].blocked:
            neighbors.append(self.maze[row - 1][col])
        if (row < self.height - 1
                and not cell.down
                and not self.maze[row + 1][col].blocked):
            neighbors.append(self.maze[row + 1][col])
        if col > 0 and not cell.left and not self.maze[row][col - 1].blocked:
            neighbors.append(self.maze[row][col - 1])
        if (col < self.width - 1
                and not cell.right
                and not self.maze[row][col + 1].blocked):
            neighbors.append(self.maze[row][col + 1])
        return neighbors

    def bfs(self,
            start: 'MazeGenerator.Cell',
            end: 'MazeGenerator.Cell') -> List['MazeGenerator.Cell']:
        """Find shortest path from start to end using BFS. Marks solution
        cells."""
        q: Deque['MazeGenerator.Cell'] = deque([start])
        visited: Set[Tuple[int, int]] = {(start.row, start.col)}
        root: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {
            (start.row, start.col): None
        }

        while q:
            current: 'MazeGenerator.Cell' = q.popleft()
            if current == end:
                path: List['MazeGenerator.Cell'] = []
                coord: Optional[Tuple[int, int]] = (end.row, end.col)
                while coord is not None:
                    r, c = coord
                    path.append(self.maze[r][c])
                    coord = root[coord]
                path.reverse()
                for cell in path:
                    cell.solution = True
                return path
            for neighbor in self.get_open_neighbors(current):
                coord = (neighbor.row, neighbor.col)
                if coord not in visited:
                    visited.add(coord)
                    root[coord] = (current.row, current.col)
                    q.append(neighbor)
        return []

    def add_extra_paths(self,
                        start: Tuple[int, int],
                        end: Tuple[int, int]) -> None:
        """Open walls around start and end positions to ensure
        accessibility."""
        for row, col in [start, end]:
            cell: 'MazeGenerator.Cell' = self.maze[row][col]
            if row > 0 and not self.maze[row - 1][col].blocked and cell.top:
                cell.top = False
                self.maze[row - 1][col].down = False
            if (row < self.height - 1
                    and not self.maze[row + 1][col].blocked
                    and cell.down):
                cell.down = False
                self.maze[row + 1][col].top = False
            if (col > 0
                    and not self.maze[row][col - 1].blocked
                    and cell.left):
                cell.left = False
                self.maze[row][col - 1].right = False
            if (col < self.width - 1
                    and not self.maze[row][col + 1].blocked
                    and cell.right):
                cell.right = False
                self.maze[row][col + 1].left = False
