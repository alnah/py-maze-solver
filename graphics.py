from enum import Enum
from tkinter import Tk, BOTH, Canvas


class FillColor(Enum):
    """Enumerate the fill colors used for drawing maze elements."""

    WHITE = "#ffffff"
    BLACK = "#000000"
    GREEN = "#00FF7F"
    RED = "#cc0000"


class Point:
    """Represent a coordinate in 2D space."""

    def __init__(self, x: float, y: float) -> None:
        """Initialize the point with given x and y coordinates."""
        self.x = x
        self.y = y


class Line:
    """Represent a line segment connecting two points."""

    def __init__(self, p1: Point, p2: Point) -> None:
        """Initialize the line with a starting and ending point."""
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, fill_color: FillColor) -> None:
        """Render the line on a canvas with the specified fill color."""
        canvas.create_line(
            self.p1.x,
            self.p1.y,
            self.p2.x,
            self.p2.y,
            fill=fill_color.value,
            width=2,
        )


class Window:
    """Provide a graphical window for maze vizualization."""

    def __init__(self, width: float, height: float) -> None:
        """Initialize with a canvas for drawing the maze."""
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(
            self.__root,
            bg=FillColor.BLACK.value,
            height=height,
            width=width,
        )
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False

    def redraw(self) -> None:
        """Refresh the window to update drawn elements."""
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        """Keep the window open until the user closes it."""
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def draw_line(self, line: Line, fill_color: FillColor = FillColor.WHITE) -> None:
        """Draw a line on the window's canvas with a given color."""
        line.draw(self.__canvas, fill_color)

    def close(self) -> None:
        """Signal the window to stop running and close."""
        self.__running = False
