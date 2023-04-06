# This will work if ran from the root folder.
import sys 
sys.path.append("delivery_network")

from graph import Graph, graph_from_file

import unittest   # The test framework

class Test_GraphCC(unittest.TestCase):
    def test_network0(self):
        g = graph_from_file("input/network.00.in")
        cc = g.connected_components()
        self.assertEqual(cc, [[1, 2, 1, 6, 8, 9, 3, 4, 10, 5, 7]])

    def test_network1(self):
        g = graph_from_file("input/network.01.in")
        cc = g.connected_components()
        self.assertEqual(cc, [[1, 2, 1, 3], [4, 5, 4, 7, 6]])

if __name__ == '__main__':
    unittest.main()
