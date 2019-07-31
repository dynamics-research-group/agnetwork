from structure import Structure
from structure import Network
from element import Boundary
from element import IrreducibleElement
from joint import Joint
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':
    network = Network()
    
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

    V,E = network.modularProduct(bridge1,bridge2)
    print(len(E))
    print(len(V))

    # print(network.maximalCliques({(1,2),(3,4),(5,6),(7,8)}, {((1,2),(3,4)),((3,4),(5,6)),((1,2),(5,6)),((5,6),(7,8))}))
    
    cliques = network.maximalCliquesBK(V,E)

    max_len = 0
    for clique in cliques:
        if len(clique) > max_len:
            max_len = len(clique)
            max_clique = [clique]
        elif len(clique) == max_len:
            max_clique.append(clique)
    
    print(max_len)
    for i, clique in enumerate(max_clique):
        print("Max clique", i+1, ":", clique)
    print(len(max_clique))

    print(cliques[0])
    print(cliques[1])
    print(len(cliques))
    
    modularProductGraph = nx.Graph()
    modularProductGraph.add_edges_from(E)
    modularProductGraph.add_nodes_from(V)

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