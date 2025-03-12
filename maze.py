from graphics import Window
from cell import Cell
import time
import random

ANIMATION_CELLS_CREATION: float = 1 / 100000
ANIMATION_MAZE_SOLVING: float = 1 / 25


class Maze:
    """Represent a maze composed of cells and manage its generation and resolution."""

    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: float,
        cell_size_y: float,
        win: Window | None = None,
        seed: int | None = None,
    ) -> None:
        """
        Initialize the maze by setting up the grid, carving paths,
        and defining entry/exit points.
        """
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells: list[list[Cell]] = []
        if seed is not None:
            self._seed = random.seed(seed)

        self._create_cells()
        if self._cells:
            self._break_entrance_and_exit()
            self._break_walls_with_dfs(0, 0)
            self._reset_cells_visited()

    def _create_cells(self) -> None:
        """Generate the grid of cells and immediately draw them for visualization."""
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i: int, j: int) -> None:
        """Render a single cell at its grid position to reflect its current wall status."""
        if self._win is None:
            return

        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y

        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y

        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate(ANIMATION_CELLS_CREATION)

    def _animate(self, animation_time: float) -> None:
        """Update the display to animate maze creation or solving process."""
        if self._win is None:
            return

        self._win.redraw()
        time.sleep(animation_time)

    def _break_entrance_and_exit(self) -> None:
        """Remove walls at the maze entry and exit."""
        entrance, exit = self._cells[0][0], self._cells[-1][-1]

        entrance.has_top_wall = False
        entrance.draw(entrance._x1, entrance._y1, entrance._x2, entrance._y2)

        exit.has_bottom_wall = False
        exit.draw(exit._x1, exit._y1, exit._x2, exit._y2)

    def _break_walls_with_dfs(self, start_i: int, start_j: int) -> None:
        """Carve out the maze paths using a randomized DFS to remove walls between cells."""
        stack = [(start_i, start_j)]
        self._cells[start_i][start_j].visited = True

        while stack:
            i, j = stack[-1]
            next_index_list = []

            # Check unvisited neighbors
            if i > 0 and not self._cells[i - 1][j].visited:  # left
                next_index_list.append((i - 1, j))
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:  # right
                next_index_list.append((i + 1, j))
            if j > 0 and not self._cells[i][j - 1].visited:  # up
                next_index_list.append((i, j - 1))
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:  # down
                next_index_list.append((i, j + 1))

            if next_index_list:
                # Choose a random neighbor
                next_i, next_j = random.choice(next_index_list)

                # Knock down the wall between (i, j) and (next_i, next_j)
                if next_i == i + 1:  # right
                    self._cells[i][j].has_right_wall = False
                    self._cells[next_i][j].has_left_wall = False
                elif next_i == i - 1:  # left
                    self._cells[i][j].has_left_wall = False
                    self._cells[next_i][j].has_right_wall = False
                elif next_j == j + 1:  # down
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[i][next_j].has_top_wall = False
                elif next_j == j - 1:  # up
                    self._cells[i][j].has_top_wall = False
                    self._cells[i][next_j].has_bottom_wall = False

                self._cells[next_i][next_j].visited = True
                self._draw_cell(next_i, next_j)
                stack.append((next_i, next_j))
            else:
                # Backtrack if no unvisited neighbors
                self._draw_cell(i, j)
                stack.pop()

    def _reset_cells_visited(self) -> None:
        """Reset the visited flag for all cells after maze generation."""
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def _solve_r(self, i: int, j: int) -> bool:
        """
        Recursively attempt to solve the maze by exploring valid neighboring cells.
        Visualize the path taken and backtracks when necessary.
        """
        self._animate(ANIMATION_MAZE_SOLVING)

        # vist the current cell
        self._cells[i][j].visited = True

        # if we are at the end cell, we are done!
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        # move left if there is no wall and it hasn't been visited
        if (
            i > 0
            and not self._cells[i][j].has_left_wall
            and not self._cells[i - 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)

        # move right if there is no wall and it hasn't been visited
        if (
            i < self._num_cols - 1
            and not self._cells[i][j].has_right_wall
            and not self._cells[i + 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)

        # move up if there is no wall and it hasn't been visited
        if (
            j > 0
            and not self._cells[i][j].has_top_wall
            and not self._cells[i][j - 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)

        # move down if there is no wall and it hasn't been visited
        if (
            j < self._num_rows - 1
            and not self._cells[i][j].has_bottom_wall
            and not self._cells[i][j + 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)

        # we went the wrong way let the previous cell know by returning False
        return False

    def solve(self) -> bool:
        """Start solving the maze from the entrance."""
        return self._solve_r(0, 0)
