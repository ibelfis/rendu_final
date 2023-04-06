from graph import graph_from_file
import unittest   # The test framework

class Test_MinimalPower(unittest.TestCase):
    def test_network0(self):
        g = graph_from_file("input/network.00.in")
        self.assertEqual(g.min_power([1, 4])[0], 25)
        self.assertEqual(g.min_power([2, 4])[0], 14)

    def test_network1(self):
        g = graph_from_file("input/network.04.in")
        self.assertEqual(g.min_power([1, 4])[0], 11)

if __name__ == '__main__':
    unittest.main()
