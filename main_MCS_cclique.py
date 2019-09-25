from structure import Structure
from structure import Network
from element import Boundary
from element import IrreducibleElement
from joint import Joint
import networkx as nx
import matplotlib.pyplot as plt
import graph_comparison as gc

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

    V, E = gc.modularProduct(bridge2, bridge3)

    modularProductGraph = nx.Graph()
    modularProductGraph.add_edges_from(E)
    modularProductGraph.add_nodes_from(V)

    nx.draw(modularProductGraph, with_labels=True)
    plt.show()

    # print(gc.maximalCliques({(1,2),(3,4),(5,6),(7,8)}, {((1,2),(3,4)),((3,4),(5,6)),((1,2),(5,6)),((5,6),(7,8))}))
    
    V1 = bridge2.nodeList()
    V2 = bridge3.nodeList()
    E1 = bridge2.edgeList()
    E2 = bridge3.edgeList()
    cEdges, dEdges = gc.findCedges(E, E1, E2)

    print("Neighbours:", gc.neighbourSet(V1, E1))

    # Print information about the inputs to the cliques algorithm
    print("Number of modular product edges:", len(E), "and vertices:", len(V))
    print("Number of c-edges:", len(cEdges),"and d-edges:", len(dEdges))
    
    print("\n###################################\n")

    cEdgeGraph = nx.Graph()
    cEdgeGraph.add_edges_from(cEdges)
    cEdgeGraph.add_nodes_from(V)

    nx.draw(cEdgeGraph, with_labels=True)
    plt.show()

    cliques_BK = gc.maximalCliquesBK(V, E)
    cliques = list(gc.maximalCliquesCedges(V, E, cEdges, dEdges))

    # Remove duplicates in cliques
    # cliques = [set(item) for item in set(frozenset(item) for item in cliques)]
    # cliques_BK = [set(item) for item in set(frozenset(item) for item in cliques_BK)]

    cliques = [set(item) for item in set(frozenset(item) for item in cliques)]

    max_cliques_BK = gc.maxCliques(cliques_BK)
    max_cliques = gc.maxCliques(cliques)

    # Print cliques for BK algorithm
    print("Largest cliques found using BK pivot")
    for i, clique in enumerate(max_cliques_BK):
        print("Max clique", i+1, ":", clique)

    print("Number of cliques:", len(cliques_BK))

    print("\n###################################\n")

    # Print cliques for c-clique algorithm
    print("Largest cliques found using c-edges")
    for i, clique in enumerate(max_cliques):
        print("Max clique", i+1, ":", clique)

    print("Number of cliques:", len(cliques))

    # cliques_no_repeat = [set(item) for item in set(frozenset(item) for item in cliques)]
    #
    # print("Number of repeated cliques:", len(cliques) - len(cliques_no_repeat))

    cliques1 = list(gc.maximalCliquesCedges(V, E, cEdges, dEdges))
    cliques2 = list(gc.maximalCliquesCedges(V, E, cEdges, dEdges))
    
    # Check that both max clique sets contain same subgraphs
    matched = sum([int(sgBK == sg) for sgBK in max_cliques_BK for sg in max_cliques])
    
    print("\n###################################\n")

    print("{0} subgraphs matched out of {1}".format(matched, len(max_cliques_BK)))

    print("\n###################################\n")

    #print(cliques)

    c_cliques = gc.check_adjacency(max_cliques, cEdges)
    for i, clique in enumerate(c_cliques):
        print("Connected cliques", i+1, ":", clique)
    
    print("\n###################################\n")

    ss = gc.mcsSimilarityScore(max_cliques[0], V1, V2)
    print("Similarity score:", round(ss, 2) , "%")