from structure import Structure
from structure import Network
from element import Boundary
from element import Beam
from joint import Joint
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':
    network = Network()

    struct1 = Structure('struct1')
    struct1.graph = {'1' : ['2'],
                     '2' : ['1','3'],
                     '3' : ['2']}
    struct1.addToNetwork()

    struct2 = Structure('struct2')
    struct2.graph = {'a' : ['b'],
                     'b' : ['a','c'],
                     'c' : ['b']}
    struct2.addToNetwork()
    
    print(network.structures['struct1'])
    print(network.structures['struct2'])
    
    modularproduct = network.modularProduct('struct1','struct2')
    # print(modularproduct['edges'])
    # print(modularproduct['nodes'])

    network.findCEdges(modularproduct['edges'],
                       network.structures['struct1']['edges'],
                       network.structures['struct2']['edges'])

    # print(network.maximalCliquesBK({(1,2),(3,4),(5,6),(7,8)}, {((1,2),(3,4)),((3,4),(5,6)),((1,2),(5,6)),((5,6),(7,8))}))
    print(network.maximalCliquesBK({'A','B','C','D'}, {('A','B'),('B','C'),('A','C'),('C','D')}))
    
    cliques = network.maximalCliquesBK(modularproduct['nodes'],modularproduct['edges'])

    print(cliques)
    # print(cliques[0])
    # print(cliques[1])
    # print(len(cliques))
    
    modularProductGraph = nx.Graph()
    modularProductGraph.add_edges_from(modularproduct['edges'])
    modularProductGraph.add_nodes_from(modularproduct['nodes'])

    nx.draw(modularProductGraph, with_labels=True)
    plt.show()