# This will work if ran from the root folder.
from graph import graph_from_file
import unittest   # The test framework

class Test_MinimalDistance(unittest.TestCase):
    def test_network0(self):
        g = graph_from_file("input/network.00.in")
        self.assertEqual(g.get_path_with_distance(1, 4), [1, 2, 3, 4])
        self.assertEqual(g.get_path_with_distance(2, 4), [2, 3, 4])

    def test_network1(self):
        g = graph_from_file("input/network.04.in")
        self.assertEqual(g.get_path_with_distance(1, 4), [1, 4])

if __name__ == '__main__':
    unittest.main()