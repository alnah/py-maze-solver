from enum import Enum
from tkinter import Tk, BOTH, Canvas


class FillColor(Enum):
    WHITE = "white"
    BLACK = "black"
    GREEN = "#00FF7F"
    RED = "#cc0000"


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, fill_color: FillColor) -> None:
        canvas.create_line(
            self.p1.x,
            self.p1.y,
            self.p2.x,
            self.p2.y,
            fill=fill_color.value,
            width=2,
        )


class Window:
    def __init__(self, width: float, height: float):
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
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def draw_line(self, line: Line, fill_color: FillColor = FillColor.WHITE) -> None:
        line.draw(self.__canvas, fill_color)

    def close(self) -> None:
        self.__running = False
