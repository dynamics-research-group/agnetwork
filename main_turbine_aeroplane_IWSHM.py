from structure import Structure
from structure import Network
from element import Boundary
from element import Beam
from joint import Joint
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':

    # Define the graph for a turbine
    turbine = Structure('Turbine')
    turbine.graph = {'A': ['D'], 
                     'B': ['D'],
                     'C': ['D'],
                     'D': ['A','B','C','E'],
                     'E': ['D','F'],
                     'F': ['E','G'],
                     'G': ['F','H'],
                     'H': ['G','I'],
                     'I': ['H','BC1','BC2'],
                     'BC1': ['I'],
                     'BC2': ['I']}

    # Define the graph for an aeroplane
    aeroplane = Structure('Aeroplane')
    aeroplane.graph = {'A': ['C'],
                       'B': ['C'], 
                       'C': ['A','B','D'],
                       'D': ['C'],
                       'E': ['F'],
                       'F': ['E','G'],
                       'G': ['F','H','M'],
                       'H': ['C','G','I','N'],
                       'I': ['H','J','O'],
                       'J': ['I','K'],
                       'K': ['J'],
                       'L': ['M'], 
                       'M': ['L','G'],
                       'N': ['H'],
                       'O': ['I','P'],
                       'P': ['O']}
    
    # Initiliase nx.Graph object
    turbineGraph = nx.Graph()
    # Add nodes and edges from turbine
    turbineGraph.add_nodes_from(turbine.nodeList())
    turbineGraph.add_edges_from(turbine.edgeList())

    # Initiliase nx.Graph object
    bridge2Graph = nx.Graph()
    # Add nodes and edges from aeroplane    
    bridge2Graph.add_nodes_from(aeroplane.nodeList())
    bridge2Graph.add_edges_from(aeroplane.edgeList())

    # Create subplots with bridge graphs
    plt.subplot(121)
    nx.draw(turbineGraph, with_labels=True)
    plt.subplot(122)
    nx.draw(bridge2Graph, with_labels=True)
    plt.show()