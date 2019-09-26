from structure import Structure
from structure import Network
from element import Boundary
from element import Element
from joint import Joint
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.clique import find_cliques

def maxCliques(cliques):
    max_len = 0
    for clique in cliques:
        if len(clique) > max_len:
            max_len = len(clique)
            max_cliques = [clique]
        elif len(clique) == max_len:
            max_cliques.append(clique)
    return max_cliques

def check_adjacency(cliques, cEdges):
    """Check that all are adjacent in the graphs"""
    c_cliques = []
    for clique in cliques:
        vi = list(clique)[0]
        v_seen = set()
        connected = is_connected(clique, v_seen, vi, cEdges)
        if connected == True:
            c_cliques.append(clique)
    return c_cliques

def is_connected(clique, v_seen, vi, cEdges):
    v_seen.add(vi)
    if len(v_seen) == len(clique): return True
    for v2 in clique:
        if v2 not in v_seen:
            if ((vi, v2) in cEdges) or ((v2, vi) in cEdges):
                    return is_connected(clique, v_seen, v2, cEdges)
    return False

if __name__ == '__main__':
    network = Network()

    struct1 = Structure('struct1')
    # struct1.graph = {'1' : ['2'],
    #                  '2' : ['1','3'],
    #                  '3' : ['2']}
    struct1.elements = {'a':[], 'b':[], 'c':[], 'd':[]}
    struct1.joints = {'1': [['a','b']], '2': [['b','c']], '3': [['b','d']]}
    struct1.addElements()
    struct1.addJoints()
    struct1.edgeList()
    struct1.addToNetwork()

    struct2 = Structure('struct2')
    # struct2.graph = {'a' : ['b'],
    #                  'b' : ['a','c'],
    #                  'c' : ['b']}
    struct2.elements = {'a':[], 'b':[], 'c':[], 'd':[], 'e':[]}
    struct2.joints = {'1': [['a','b']], '2': [['b', 'c']], '3': [['b', 'd']], '4': [['d','e']], '5': [['c','e']]}
    struct2.addElements()
    struct2.addJoints()
    struct2.edgeList()
    struct2.addToNetwork()

    V, E = network.modularProduct(struct1,struct2)

    modularProductGraph = nx.Graph()
    modularProductGraph.add_edges_from(E)
    modularProductGraph.add_nodes_from(V)

    nx.draw(modularProductGraph, with_labels=True)
    plt.show()

    # cliques = network.maximalCliquesBK(V,E)
    # print(modularproduct['edges'])
    # print(modularproduct['nodes'])

    cEdges, dEdges = network.findCedges(E, struct1.edgeList(), struct2.edgeList())
    cEdgeGraph = nx.Graph()
    cEdgeGraph.add_edges_from(cEdges)
    cEdgeGraph.add_nodes_from(V)

    nx.draw(cEdgeGraph, with_labels=True)
    plt.show()

    # print(network.maximalCliquesBK({(1,2),(3,4),(5,6),(7,8)}, {((1,2),(3,4)),((3,4),(5,6)),((1,2),(5,6)),((5,6),(7,8))}))
    # print(network.maximalCliquesBK({'A','B','C','D'}, {('A','B'),('B','C'),('A','C'),('C','D')}))
    
    cliques_BK = network.maximalCliquesBK(V, E)
    cliques = list(network.maximalCliquesCedges(V, E, cEdges, dEdges))

    # Remove duplicates in cliques
    cliques = [set(item) for item in set(frozenset(item) for item in cliques)]
    cliques_BK = [set(item) for item in set(frozenset(item) for item in cliques_BK)]

    max_cliques_BK = maxCliques(cliques_BK)
    max_cliques = maxCliques(cliques)

    # Print cliques for BK algorithm
    print("Largest cliques found using BK pivot")
    for i, clique in enumerate(max_cliques_BK):
        print("Max clique", i+1, ":", clique)

    print("\n###################################\n")

    # Print cliques for c-clique algorithm
    print("Largest cliques found using c-edges")
    for i, clique in enumerate(max_cliques):
        print("Max clique", i+1, ":", clique)
    
    print("\n###################################\n")

    # Check that both max clique sets contain same subgraphs
    matched = sum([int(sgBK == sg) for sgBK in max_cliques_BK for sg in max_cliques])
    
    print("{0} subgraphs matched out of {1}".format(matched, len(max_cliques_BK)))

    print("\n###################################\n")

    print("Number of cliques found using BK:", len(cliques_BK))
    for i, clique in enumerate(cliques_BK):
        print("Clique", i+1, ":", clique)

    print("\n###################################\n")

    print("Number of cliques found using c-cliques:", len(cliques))
    for i, clique in enumerate(cliques):
        print("Clique", i+1, ":", clique)