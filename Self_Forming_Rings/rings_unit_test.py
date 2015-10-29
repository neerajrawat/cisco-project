import unittest
import networkx as nx
from rings import *

class TestRingsMethods(unittest.TestCase):

	def test_isCycle(self):
		g = nx.Graph()
		g.add_edges_from([(1,2),(2,3),(3,1)]) # triangle
		self.assertTrue(g)
		g.clear()
		g.add_edges_from([(1,2),(2,3),(3,1),(2,4),(3,4)]) # two triangles, one common edge
		self.assertFalse(g)
		g.clear()
		g.add_edges_from([(1,2),(2,3),(3,1),(5,4),(6,4),(5,6)]) # two disconnected triangles
		self.assertFalse(g)
		g.clear()
		g.add_edges_from([(1,2),(2,3),(3,1),(2,4),(2,5),(4,5)]) # two triangles, one common node
		self.assertFalse(g)
		g.clear()

	def test_getCycleBasis(self):
		pass

	def test_getALlRings(self):
		pass

if __name__ == '__main__':
	unittest.main()


