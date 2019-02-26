import unittest
from structure import Network
from structure import Structure
from unittest.mock import patch

class TestStructreClass(unittest.TestCase):

    def setUp(self):
        # Create an instance of the Structure class 
        self.struct = Structure('struct')
        self.assertEqual(self.struct.graph, {})
        self.struct.graph = {}

    def test_init(self):
        # Check that Structure initialised correctly
        self.assertEqual(self.struct.structureID, 'struct')
        self.assertEqual(self.struct.nodes, {})
        self.assertEqual(self.struct.elements['struct'], {})

    def test_addNode(self):
        # Check that node is added to graph correctly
        self.struct.addNode('a')
        self.assertEqual(self.struct.graph['a'], [])
        # Check that no new node is created if it already exists
        self.assertIsNone(self.struct.addNode('a'))

    def test_addEdge(self):
        # Check that the function adds edges correctly
        self.struct.graph = {'a': [], 'b': []}
        self.struct.addEdge(['a', 'b'])
        self.assertEqual(self.struct.graph['a'], ['b'])
        self.assertEqual(self.struct.graph['b'], ['a'])
        # Check that if only one node in an edge exits, it is not possible to add an edge
        with self.assertRaisesRegex(KeyError, "first node not found in graph"):
            self.struct.addEdge(['c', 'a'])
        with self.assertRaisesRegex(KeyError, "second node not found in graph"):
            self.struct.addEdge(['a', 'c'])

    def test_nodeList(self):
        # Check that nodeList returns the full list of nodes
        self.struct.graph = {'a': [],'b': [],'c': []}
        self.assertEqual(self.struct.nodeList(), ['a', 'b', 'c'])
    
    def test_edgeList(self):
        # Check that edgeList returns the full list of edges
        self.struct.graph = {'a': ['b'],
                             'b': ['a','c'],
                             'c': ['b']}
        self.assertEqual(self.struct.edgeList(), [{'a','b'}, {'b','c'}])

    def test_addElements(self):
        # Check that the full list of nodes is added
        self.struct.elements['struct'] = {'a': [], 'b': [], 'c':[]}
        self.assertEqual(self.struct.addElements(), ['a', 'b', 'c'])
        # Check that addNodes was called correctly
        self.assertEqual(self.struct.graph, {'a': [],'b': [],'c': []})

    def test_addJoints(self):
        # Check that graph attribute is modified correctly when adding joints
        self.struct.graph = {'a': [], 'b': [], 'c': []}
        self.struct.joints['struct'] = {1: [['a','b'], 1], 
                                        2: [['b','c'], 1]}
        self.struct.addJoints()
        self.assertEqual(self.struct.graph, {'a': ['b'], 'b': ['a','c'], 'c': ['b']})
        # Check that adding a joint where both nodes do not exist in the graph gives an error
        self.struct.joints['struct'][3] = [['c','d'], 1]
        with self.assertRaisesRegex(ValueError, "nodes not found in graph for jointID=3"):
            self.struct.addJoints()
    
    # def test_graphSeperation(self):
    #     # Test whether two seperate structures can have seperate lists of edges and elements
    #     self.struct.elements = {'a': [], 'b': []}
    #     self.struct.joints = {1: [['a','b'], 1]}
    #     self.struct2 = Structure("struct2")
    #     self.struct2.elements = {'c': [], 'd': []}
    #     self.struct2.joints = {1: [['c','d'], 1]}
    #     self.assertNotEqual(self.struct.joints, self.struct2.joints)
            
if __name__ == '__main__':
    unittest.main()