from structure import Structure
from structure import Network
from element import Boundary
from element import Element
from joint import Joint
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.clique import find_cliques

if __name__ == '__main__':
    network = Network()

    struct1 = Structure('struct1')
    # struct1.graph = {'1' : ['2'],
    #                  '2' : ['1','3'],
    #                  '3' : ['2']}
    struct1.elements = {'a':[], 'b':[], 'c':[]}
    struct1.joints = {'1': [['a','b']], '2': [['b','c']]}
    struct1.addElements()
    struct1.addJoints()
    struct1.edgeList()
    struct1.addToNetwork()

    print(struct1.nodes)

    struct2 = Structure('struct2')
    # struct2.graph = {'a' : ['b'],
    #                  'b' : ['a','c'],
    #                  'c' : ['b']}
    struct2.elements = {'a':[], 'b':[], 'c':[]}
    struct2.joints = {'1': [['a','b']], '2': [['b', 'c']]}
    struct2.addElements()
    struct2.addJoints()
    struct2.edgeList()
    struct2.addToNetwork()
    
    print(network.structures['struct1'])
    print(network.structures['struct2'])
    
    print(struct1.nodes)

    V, E = network.modularProduct(struct1,struct2)

    modularProductGraph = nx.Graph()
    modularProductGraph.add_edges_from(E)
    modularProductGraph.add_nodes_from(V)

    nx.draw(modularProductGraph, with_labels=True)
    plt.show()

    # cliques = network.maximalCliquesBK(V,E)
    # print(modularproduct['edges'])
    # print(modularproduct['nodes'])

    cEdges = network.findCedges(E, struct1.edgeList(), struct2.edgeList())
    cEdgeGraph = nx.Graph()
    cEdgeGraph.add_edges_from(cEdges)
    cEdgeGraph.add_nodes_from(V)

    nx.draw(cEdgeGraph, with_labels=True)
    plt.show()

    # print(network.maximalCliquesBK({(1,2),(3,4),(5,6),(7,8)}, {((1,2),(3,4)),((3,4),(5,6)),((1,2),(5,6)),((5,6),(7,8))}))
    # print(network.maximalCliquesBK({'A','B','C','D'}, {('A','B'),('B','C'),('A','C'),('C','D')}))
    
    cliques = network.maximalCliquesCedges(V, E, cEdges)

    print(cliques[0][:3])

    # print(cliques[0])
    # print(cliques[1])
    # print(len(cliques))