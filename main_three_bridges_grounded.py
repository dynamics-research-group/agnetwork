from structure import Structure
from structure import Network
from element import Boundary
from element import Beam
from joint import Joint
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':

    # Define the graph for bridge1
    bridge1 = Structure('Bridge1')
    bridge1.graph = {1 : ['A','A','B'],
                    'A': [1, 'B', 1], 
                    'B': ['A', 1]}

    # Define the graph for bridge2
    bridge2 = Structure('Bridge2')
    bridge2.graph = {1: ['A','B','C','D'],
                    'A': [1, 'C', 'B'], 
                    'C': ['A', 'D', 1],
                    'B': ['A', 1], 
                    'D': ['C', 1]}

    # Define the graph for bridge3
    bridge3 = Structure('Bridge3')
    bridge3.graph = {1: ['A'], 
                     2: ['B'], 
                     3: ['D'],
                     4: ['F'], 
                     5: ['E'], 
                    'A': [1, 'C', 'B'], 
                    'C': ['A', 'D', 'E'],
                    'B': ['A', 2], 
                    'D': ['C', 3],
                    'E': ['C','F', 5],
                    'F': ['E', 4]}
    
    # Initiliase nx.Graph object
    bridge1Graph = nx.Graph()
    # Add nodes and edges from bridge1
    bridge1Graph.add_nodes_from(bridge1.nodeList())
    bridge1Graph.add_edges_from(bridge1.edgeList())

    # Initiliase nx.Graph object
    bridge2Graph = nx.Graph()
    # Add nodes and edges from bridge2    
    bridge2Graph.add_nodes_from(bridge2.nodeList())
    bridge2Graph.add_edges_from(bridge2.edgeList())
    
    # Initiliase nx.Graph object
    bridge3Graph = nx.Graph()
    # Add nodes and edges from bridge3
    bridge3Graph.add_nodes_from(bridge3.nodeList())
    bridge3Graph.add_edges_from(bridge3.edgeList())

    # Create subplots with bridge graphs
    plt.subplot(121)
    nx.draw(bridge1Graph, with_labels=True)
    plt.subplot(122)
    nx.draw(bridge2Graph, with_labels=True)
    plt.show()

    """
    plt.subplot(131)
    nx.draw(bridge1Graph, with_labels=True)
    plt.subplot(132)
    nx.draw(bridge2Graph, with_labels=True)
    plt.subplot(133)
    nx.draw(bridge3Graph, with_labels=True)
    plt.show()
    """