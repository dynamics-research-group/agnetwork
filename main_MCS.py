from structure import Structure
from structure import Network
from element import Boundary
from element import Beam
from joint import Joint
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':
    network = Network()
    """
    bridge1 = Structure('Bridge1')
    bridge1.graph = {'1' : ['A'],
                     '2' : ['B'],
                     '3' : ['A'], 
                     'A': ['1', 'B', '3'], 
                     'B': ['A', '2']}

    bridge2 = Structure('Bridge2')
    bridge2.graph = {'1': ['A'], 
                     '2': ['B'], 
                     '3': ['D'],
                     '4': ['C'], 
                     'A': ['1', 'C', 'B'], 
                     'C': ['A', 'D', '4'],
                     'B': ['A', '2'], 
                     'D': ['C', '3']}

    bridge3 = Structure('Bridge3')
    bridge3.graph = {'1': ['A'], 
                     '2': ['B'], 
                     '3': ['D'],
                     '4': ['F'], 
                     '5': ['E'], 
                     'A': ['1', 'C', 'B'], 
                     'C': ['A', 'D', 'E'],
                     'B': ['A', '2'], 
                     'D': ['C', '3'],
                     'E': ['C','F', '5'],
                     'F': ['E', '4']}
    
    bridge1.addToNetwork()
    bridge2.addToNetwork()
    bridge3.addToNetwork()

    modularproduct = network.modularProduct('Bridge1','Bridge2')
    """

    struct1 = Structure('struct1')
    struct1.graph = {'1' : ['D'],
                     'D' : ['1','3'],
                     '3' : ['D']}
    struct1.addToNetwork()

    struct2 = Structure('struct2')
    struct2.graph = {'1' : ['2'],
                     '2' : ['1','A'],
                     'A' : ['2']}
    struct2.addToNetwork()
    
    print(network.structures['struct1'])
    print(network.structures['struct2'])
    
    modularproduct = network.modularProduct('struct1','struct2')
    print(modularproduct['edges'])
    print(modularproduct['nodes'])
 
    modularProductGraph = nx.Graph()
    modularProductGraph.add_edges_from(modularproduct['edges'])
    modularProductGraph.add_nodes_from(modularproduct['nodes'])

    nx.draw(modularProductGraph, with_labels=True)
    plt.show()

    """
    bridge1Graph = nx.Graph()
    bridge1Graph.add_nodes_from(bridge1.nodeList())
    bridge1Graph.add_edges_from(bridge1.edgeList())

    bridge2Graph = nx.Graph()
    bridge2Graph.add_nodes_from(bridge2.nodeList())
    bridge2Graph.add_edges_from(bridge2.edgeList())
    
    bridge3Graph = nx.Graph()
    bridge3Graph.add_nodes_from(bridge3.nodeList())
    bridge3Graph.add_edges_from(bridge3.edgeList())

    plt.subplot(131)
    nx.draw(bridge1Graph, with_labels=True)
    plt.subplot(132)
    nx.draw(bridge2Graph, with_labels=True)
    plt.subplot(133)
    nx.draw(bridge3Graph, with_labels=True)
    plt.show()
    """