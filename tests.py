import unittest
from maze import Maze


class Tests(unittest.TestCase):
    def test_empty_maze(self):
        num_cols, num_rows = 0, 0
        maze = Maze(0, 0, num_cols, num_rows, 10, 10)
        self.assertEqual(len(maze._cells), num_cols)

    def test_maze_create_cells(self):
        testCases = [
            {
                "num_cols": 10,
                "num_rows": 10,
            },
            {
                "num_cols": 12,
                "num_rows": 10,
            },
            {
                "num_cols": 10,
                "num_rows": 12,
            },
            {
                "num_cols": 100,
                "num_rows": 100,
            },
        ]
        for tc in testCases:
            maze = Maze(0, 0, tc["num_rows"], tc["num_cols"], 10, 10)
            self.assertEqual(len(maze._cells), tc["num_cols"])
            self.assertEqual(len(maze._cells[0]), tc["num_rows"])

    def test_broken_entrance_and_exit(self):
        num_cols, num_rows = 10, 10
        maze = Maze(0, 0, num_rows, num_cols, 10, 10)
        entrance, exit = maze._cells[0][0], maze._cells[-1][-1]
        self.assertFalse(entrance.has_top_wall)
        self.assertFalse(exit.has_bottom_wall)

    def test_reset_cells_visited(self):
        num_cols, num_rows = 10, 10
        maze = Maze(0, 0, num_cols, num_rows, 10, 10, seed=0)
        for i in range(num_cols):
            for j in range(num_rows):
                self.assertFalse(maze._cells[i][j].visited)


if __name__ == "__main__":
    unittest.main()
