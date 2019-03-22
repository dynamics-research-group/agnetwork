import unittest
from structure import Network
from structure import Structure
from unittest.mock import patch

class TestNetworkClass(unittest.TestCase):

    def setUp(self):
        # Create an instance of the Network class
        self.network = Network()

    def test_modularProduct(self):
        # Create the graph for the first structure
        self.struct1 = Structure('struct1')
        self.struct1.graph = {'1' : ['D'],
                              'D' : ['1','3'],
                              '3' : ['D']}
        # Create the graph for the second structure
        self.struct2 = Structure('struct2')
        self.struct2.graph = {'1' : ['2'],
                              '2' : ['1','A'],
                              'A' : ['2']}
        # Add the two structures to the network
        self.struct1.addToNetwork()
        self.struct2.addToNetwork()
        # Calculate the modular product of the two structures
        self.modularproduct = self.network.modularProduct('struct1','struct2')
        self.assertCountEqual(self.modularproduct['nodes'], {('D', '2'), ('D', '1'), ('1', 'A'), ('3', 'A'), ('1', '2'), 
                                                             ('3', '1'), ('3', '2'), ('D', 'A'), ('1', '1')})
        # self.assertCountEqual(self.modularproduct['edges'], {(('3', 'A'), ('1', '1')), (('D', '2'), ('3', 'A')), (('3', '2'), ('D', '1')), 
        #                                                      (('1', '2'), ('D', 'A')), (('1', '2'), ('D', '1')), (('D', '2'), ('1', '1')), 
        #                                                      (('3', '1'), ('1', 'A')), (('D', '2'), ('3', '1')), (('D', 'A'), ('3', '2')), 
        #                                                      (('D', '2'), ('1', 'A'))})

    def test_neighbourSet(self):
        self.edges = self.network.structures['struct1']['edges']
        self.nodes = self.network.structures['struct1']['nodes']
        self.neighbours = self.network.neighbourSet(self.nodes, self.edges)
        self.assertEqual(self.neighbours, {'1' : ['D'], 'D' : ['1','3'], '3' : ['D']})

class TestStructreClass(unittest.TestCase):

    def setUp(self):
        # Create an instance of the Structure class 
        self.struct = Structure('struct')
        self.assertEqual(self.struct.graph, {})
        self.struct.graph = {}

    def test_init(self):
        # Check that Structure initialised correctly
        self.assertEqual(self.struct.structureID, 'struct')
        self.assertEqual(self.struct.nodes, None)
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
    
    def test_addToNetwork(self):
        # Check that the structure graph is correctly added to the network structure list
        self.struct.graph = {'a': ['b'], 'b': ['a','c'], 'c': ['b']}
        self.struct.addToNetwork()
        self.assertEqual(Network.structures['struct']['nodes'], ['a','b','c'])
        self.assertEqual(Network.structures['struct']['edges'], [{'a','b'},{'b','c'}])
    
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