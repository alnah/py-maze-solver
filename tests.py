import unittest
from maze import Maze


class Tests(unittest.TestCase):
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

    def test_empty_maze(self):
        maze = Maze(0, 0, 0, 0, 10, 10)
        self.assertEqual(len(maze._cells), 0)


if __name__ == "__main__":
    unittest.main()
