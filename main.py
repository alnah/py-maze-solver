from graphics import FillColor, Line, Point, Window


def main():
    win = Window(800, 600)

    win.draw_line(Line(Point(0, 200), Point(200, 0)), FillColor.BLACK)

    win.wait_for_close()


if __name__ == "__main__":
    main()
