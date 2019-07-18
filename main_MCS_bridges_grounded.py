from structure import Structure
from structure import Network
from element import Boundary
from element import Beam
from joint import Joint
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':
    network = Network()
    
    # Define the graph for bridge1
    bridge1 = Structure('Bridge1')
    bridge1.graph = {'1' : ['A','A','B'],
                    'A': ['1', 'B', '1'], 
                    'B': ['A', '1']}

    # Define the graph for bridge2
    bridge2 = Structure('Bridge2')
    bridge2.graph = {'1': ['A','B','C','D'],
                    'A': ['1', 'C', 'B'], 
                    'C': ['A', 'D', '1'],
                    'B': ['A', '1'], 
                    'D': ['C', '1']}

    # Define the graph for bridge3
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
    
    # Add all three bridge to the network of structures
    bridge1.addToNetwork()
    bridge2.addToNetwork()
    bridge3.addToNetwork()

    # Find the modular product of bridge1 and bridge2
    modularproduct = network.modularProduct('Bridge1','Bridge2')
    # Print the number of edges in the modular product
    print(len(modularproduct['edges']))
    # Print the number of nodes in the modular product
    print(len(modularproduct['nodes']))

    # print(network.maximalCliques({(1,2),(3,4),(5,6),(7,8)}, {((1,2),(3,4)),((3,4),(5,6)),((1,2),(5,6)),((5,6),(7,8))}))
    
    # Find the maximal cliques (and hence common subgraphs) in the modular product
    cliques = network.maximalCliques(modularproduct['nodes'],modularproduct['edges'])

    # Find the maximum cliques in the modular product. These represent the maximum common subgraphs
    max_len = 0
    for clique in cliques:
        if len(clique) > max_len:
            max_len = len(clique)
            max_clique = [clique]
        elif len(clique) == max_len:
            max_clique.append(clique)
    
    # Print the size of the maximum clique
    print(max_len)
    # Print the list of maxmum cliques
    print("Maximum cliques are: " + str(max_clique))
    # Print the number of maximum cliques
    print(len(max_clique))

    # Print the first clique
    print(cliques[0])
    # Print the second clique
    print(cliques[1])
    # Print the total number of cliques
    print(len(cliques))
    
    # Initialise the modular product graph as an nx.Graph object
    modularProductGraph = nx.Graph()
    # Add edge information from the modular product graph
    modularProductGraph.add_edges_from(modularproduct['edges'])
    # Add node information from the modular product
    modularProductGraph.add_nodes_from(modularproduct['nodes'])

    # Draw and show the modular product graph
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