# This will work if ran from the root folder.
import sys 
sys.path.append("delivery_network")

from graph import Graph, graph_from_file

import unittest   # The test framework

class Test_Kruskal(unittest.TestCase):
    def test_network00(self):
        g = graph_from_file("input/network.00.in")
        temp=g.kruskal()
        self.assertEqual(temp.nodes, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(temp.graph, {1: [[8, 0, 1], [2, 11, 1], [6, 12, 1]], 2: [[5, 4, 1], [3, 10, 1], [1, 11, 1]], 3: [[4, 4, 1], [2, 10, 1]], 4: [[3, 4, 1], [10, 4, 1]], 5: [[2, 4, 1], [7, 14, 1]], 6: [[1, 12, 1]], 7: [[5, 14, 1]], 8: [[1, 0, 1], [9, 14, 1]], 9: [[8, 14, 1]], 10: [[4, 4, 1]]})

    def test_network01(self):
        g = graph_from_file("input/network.01.in")
        temp=g.kruskal()
        self.assertEqual(temp.nodes, [1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(temp.graph, {1: [[2, 1, 1]], 2: [[1, 1, 1], [3, 1, 1]], 3: [[2, 1, 1]], 4: [[5, 1, 1]], 5: [[4, 1, 1], [7, 1, 1]], 6: [[7, 1, 1]], 7: [[6, 1, 1], [5, 1, 1]]})

    def test_network02(self):
        g = graph_from_file("input/network.01.in")
        temp=g.kruskal()
        print(temp.nodes)
        print(temp.graph)
        self.assertEqual(temp.nodes, [1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(temp.graph, {1: [[2, 1, 1]], 2: [[1, 1, 1], [3, 1, 1]], 3: [[2, 1, 1]], 4: [[5, 1, 1]], 5: [[4, 1, 1], [7, 1, 1]], 6: [[7, 1, 1]], 7: [[6, 1, 1], [5, 1, 1]]})

if __name__ == '__main__':
    unittest.main()