import unittest
from structure import Structure
from unittest.mock import patch

class TestStructreClass(unittest.TestCase):

    def setUp(self):
        # Create an instance of the Structure class and check that it initialised correctly
        self.struct = Structure("struct")
        assert(self.struct.structureID == "struct")
        assert(self.struct.graph == {})
        assert(self.struct.nodes == {})
        assert(self.struct.elements == {})

    def tearDown(self):
        pass

    def test_AddNode(self):
        # Check that node is added to graph correctly
        self.struct.addNode('a')
        self.assertEqual(self.struct.graph['a'], [])
        # Check that no new node is created if it already exists
        self.assertIsNone(self.struct.addNode('a'))

    def test_AddEdge(self):
        # Check that the function adds edges correctly
        self.struct.graph = {'a': [], 'b': []}
        self.struct.addEdge(['a', 'b'])
        self.assertEqual(self.struct.graph['a'], ['b'])
        self.assertEqual(self.struct.graph['b'], ['a'])
        # Check that if only one node in an edge exits, it is not possible to add an edge
        with self.assertRaisesRegex(KeyError, "First node not found in graph"):
            self.struct.addEdge(['c', 'a'])
        with self.assertRaisesRegex(KeyError, "Second node not found in graph"):
            self.struct.addEdge(['a', 'c'])

    def test_NodeList(self):
        # Check that nodeList returns the full list of nodes
        self.struct.graph = {'a': [],'b': [],'c': []}
        self.assertEqual(self.struct.nodeList(), ['a', 'b', 'c'])
    
    def test_EdgeList(self):
        # Check that edgeList returns the full list of edges
        self.struct.graph = {'a': ['b'],
                             'b': ['a','c'],
                             'c': ['b']}
        self.assertEqual(self.struct.edgeList(), [{'a','b'}, {'b','c'}])

    def test_addElements(self):
        # Check that the full list of nodes is added
        self.struct.elements = {'a': [], 'b': [], 'c':[]}
        self.assertEqual(self.struct.addElements(), ['a', 'b', 'c'])
        # Check that addNodes was called correctly
        self.assertEqual(self.struct.graph, {'a': [],'b': [],'c': []})

    def test_addJoints(self):
        # Check that graph attribute is modified correctly when adding joints
        self.struct.graph = {'a': [], 'b': [], 'c': []}
        self.struct.joints = {1: [['a','b'], 1], 
                              2: [['b','c'], 1]}
        self.struct.addJoints()
        self.assertEqual(self.struct.graph, {'a': ['b'], 'b': ['a','c'], 'c': ['b']})
        # Check that adding a joint where both nodes do not exist in the graph gives an error
        self.struct.joints[3] = [['c','d'], 1]
        with self.assertRaisesRegex(ValueError, "Nodes not found in graph for jointID=3"):
            self.struct.addJoints()
            
if __name__ == '__main__':
    unittest.main()