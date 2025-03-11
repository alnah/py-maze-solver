from graphics import Window, Point, Line, FillColor


class Cell:
    def __init__(self, win: Window | None = None) -> None:
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = 0.0
        self._x2 = 0.0
        self._y1 = 0.0
        self._y2 = 0.0
        self._win = win

    def draw(self, x1: float, y1: float, x2: float, y2: float) -> None:
        def set_fill_color(has_wall: bool) -> FillColor:
            if not has_wall:
                return FillColor.WHITE
            return FillColor.BLACK

        self._x1, self._y1, self._x2, self._y2 = x1, y1, x2, y2

        left_line = Line(Point(x1, y1), Point(x1, y2))
        top_line = Line(Point(x1, y1), Point(x2, y1))
        right_line = Line(Point(x2, y1), Point(x2, y2))
        bottom_line = Line(Point(x1, y2), Point(x2, y2))

        line_to_has_wall = dict(
            zip(
                [left_line, top_line, right_line, bottom_line],
                [
                    self.has_left_wall,
                    self.has_top_wall,
                    self.has_right_wall,
                    self.has_bottom_wall,
                ],
            )
        )

        for line, has_wall in line_to_has_wall.items():
            if self._win is not None:
                self._win.draw_line(line, set_fill_color(has_wall))

    def draw_move(self, to_cell: "Cell", undo: bool = False) -> None:
        if not self._x1 or not self._x2 or not self._y1 or not self._y2:
            return

        half_length = abs(self._x2 - self._x1) // 2
        x_center = half_length + self._x1
        y_center = half_length + self._y1

        if not to_cell._x1 or not to_cell._x2 or not to_cell._y1 or not to_cell._y2:
            return

        half_length2 = abs(to_cell._x2 - to_cell._x1) // 2
        x_center2 = half_length2 + to_cell._x1
        y_center2 = half_length2 + to_cell._y1

        fill_color = FillColor.RED
        if undo:
            fill_color = FillColor.GREY

        line = Line(Point(x_center, y_center), Point(x_center2, y_center2))
        if self._win is None:
            raise ValueError("Cell instance expects a Window, but got None")

        self._win.draw_line(line, fill_color)
