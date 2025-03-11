from graphics import Window
from cell import Cell
import time

ANIMATION_TIME: float = 0.01


class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: float,
        cell_size_y: float,
        win: Window | None = None,
    ) -> None:
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells: list[list[Cell]] = []
        self._create_cells()

    def _create_cells(self) -> None:
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

        if self._cells:
            self._break_entrance_and_exit()

    def _break_entrance_and_exit(self) -> None:
        entrance, exit = self._cells[0][0], self._cells[-1][-1]

        entrance.has_top_wall = False
        entrance.draw(entrance._x1, entrance._y1, entrance._x2, entrance._y2)

        exit.has_bottom_wall = False
        exit.draw(exit._x1, exit._y1, exit._x2, exit._y2)

    def _draw_cell(self, i: int, j: int) -> None:
        if self._win is None:
            return

        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y

        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y

        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self) -> None:
        if self._win is None:
            return

        self._win.redraw()
        time.sleep(ANIMATION_TIME)
