from structure import Structure
from structure import Network
from element import Boundary
from element import IrreducibleElement
from joint import Joint
from networkx.algorithms.approximation.clique import max_clique
from networkx.algorithms.clique import find_cliques
import networkx as nx
import matplotlib.pyplot as plt
import time

def maxCliques(cliques):
    max_len = 0
    for clique in cliques:
        if len(clique) > max_len:
            max_len = len(clique)
            max_cliques = [clique]
        elif len(clique) == max_len:
            max_cliques.append(clique)
    return max_cliques

# def check_adjacency(cliques, E1, E2):
#     """Check that all are adjacent in the graphs"""
#     c_cliques = []
#     for clique in cliques:
#         vi = list(clique)[0]
#         v_seen = set()
#         connected = is_connected(clique, v_seen, vi, E1, E2)
#         if connected == True:
#             c_cliques.append(clique)
#     return c_cliques

# def is_connected(clique, v_seen, vi, E1, E2):
#     v_seen.add(vi)
#     if len(v_seen) == len(clique): return True
#     for v2 in clique:
#         for vi in v_seen:
#             if v2 not in v_seen:
#                 if ({vi[0], v2[0]} in E1) or ({v2[0], vi[0]} in E1):
#                     if ({vi[1], v2[1]} in E2) or ({v2[1], vi[1]} in E2):
#                         return is_connected(clique, v_seen, v2, E1, E2)
#     return False

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
        for vi in v_seen:
            if v2 not in v_seen:
                if ((vi, v2) in cEdges) or ((v2,vi) in cEdges):
                    return is_connected(clique, v_seen, v2, cEdges)
    return False

if __name__ == '__main__':
    '''This code creates the attributed graph for two
    separate structures and performs a similarity
    comparison between them. This work will go into
    the IMAC paper.'''
    network = Network()
    # Define the graph for a turbine
    turbine1 = Structure('Turbine1')
    turbine1.elements = {'A': ['FRP',      'Aerofoil'], 
                         'B': ['FRP',      'Aerofoil'],
                         'C': ['FRP',      'Aerofoil'],
                         'D': ['FRP',      'Complex'],
                         'E': ['FRP',      'Complex'],
                         'F': ['Metal',    'Cylindrical beam'],
                         'G': ['Metal',    'Cylindrical beam'],
                         'H': ['Metal',    'Cylindrical beam'],
                         'I': ['Concrete', 'Cylindrical plate'],
                         '1': ['Ground']}
    turbine1.joints = {'1': [['A','D'], [8, 15, 235.75], 'Bearing', ['x','y','z'], ['y','z']],
                       '2': [['B','D'], [8, 14, 254],    'Bearing', ['x','y','z'], ['y','z']],
                       '3': [['C','D'], [8, 16, 254],    'Bearing', ['x','y','z'], ['y','z']],
                       '4': [['D','E'], [10, 15, 253],   'Bearing', ['x','y','z'], ['x','y']],
                       '5': [['E','F'], [15, 15, 250],   'Bearing', ['x','y','z'], ['x','y']],
                       '6': [['F','G'], [15, 15, 183],   'Bolted'],
                       '7': [['G','H'], [15, 15, 105],   'Bolted'],
                       '8': [['H','I'], [15, 15, 5],     'Bolted'],
                       '9': [['I','1'], [15, 15, 0],     'Soil']}
    turbine1.addElements()
    turbine1.addJoints()
    turbine1.edgeList()

    # Define the graph for an 747
    aeroplane1 = Structure('Aeroplane1')
    aeroplane1.elements = {'A1': ['FRP',      'Truncated cone'],
                           'A2': ['FRP',      'Cylindrical beam'],
                           'A3': ['FRP',      'Cone'],
                           'B' : ['FRP',      'Aerofoil'], 
                           'C' : ['FRP',      'Complex'],
                           'D' : ['Assembly', 'Cylinder'],
                           'E' : ['FRP',      'Complex'],
                           'F' : ['Assembly', 'Cylinder'],
                           'G' : ['FRP',      'Aerofoil'],
                           'H' : ['FRP',      'Complex'],
                           'I' : ['Assembly', 'Cylinder'],
                           'J' : ['FRP',      'Complex'],
                           'K' : ['Assembly', 'Cylinder'],
                           'L' : ['FRP',      'Aerofoil'], 
                           'M' : ['FRP',      'Aerofoil'],
                           'N' : ['FRP',      'Aerofoil'],
                           'O' : ['Assembly', 'Assembly'],
                           'P' : ['Assembly', 'Assembly'],
                           '1' : ['Ground']}

    aeroplane1.joints = {'1':  [['A1','A2'], [34.2, 14.68, 5.165], 'Perfect'],
                         '2':  [['A2','A3'], [34.2, 60.96, 5.165], 'Perfect'],
                         '3':  [['A2','B'],  [32.2, 29.79, 2.89],  'Lug'],
                         '4':  [['B', 'C'],  [13.2, 42.67, 4.74],  'Complex'],
                         '5':  [['C', 'D'],  [13.2, 40.17, 4.74],  'Complex'],
                         '6':  [['B', 'E'],  [23.2, 30.79, 3.57],  'Complex'],
                         '7':  [['E', 'F'],  [23.2, 28.29, 3.57],  'Complex'],
                         '8':  [['A2','G'],  [36.2, 29.79, 2.89],  'Lug'],
                         '9':  [['G', 'H'],  [45.2, 30.79, 3.57],  'Complex'],
                         '10': [['H', 'I'],  [45.2, 28.29, 3.57],  'Complex'],
                         '11': [['G', 'J'],  [55.2, 42.67, 4.74],  'Complex'],
                         '12': [['J', 'K'],  [55.2, 40.17, 4.74],  'Complex'],
                         '13': [['A3','L'],  [33.2, 68.58, 7.55],  'Lug'],
                         '14': [['A3','M'],  [35.2, 68.58, 7.55],  'Lug'],
                         '15': [['A3','N'],  [34.2, 64.58, 9.16],  'Lug'],
                         '16': [['A1','O'],  [34.2, 7.75,  1.75],  'Complex'],
                         '17': [['A2','P'],  [34.2, 29.67, 1.75],  'Complex'],
                         '18': [['O', '1'],  [34.2, 7.75,  0],     'Friction'],
                         '19': [['P', '1'],  [34.2, 29.67, 0],     'Friction']}
    aeroplane1.addElements()
    aeroplane1.addJoints()
    aeroplane1.edgeList()

    # Define the graph for a Cessna 172
    aeroplane2 = Structure('Aeroplane1')
    aeroplane2.elements = {'A1': ['FRP',      'Truncated cone'],
                           'A2': ['FRP',      'Cylindrical beam'],
                           'A3': ['FRP',      'Cone'],
                           'B' : ['FRP',      'Aerofoil'], 
                           'C' : ['FRP',      'Complex'],
                           'D' : ['Assembly', 'Cylinder'],
                           'E' : ['FRP',      'Complex'],
                           'F' : ['Assembly', 'Cylinder'],
                           'G' : ['FRP',      'Aerofoil'],
                           'H' : ['FRP',      'Complex'],
                           'I' : ['Assembly', 'Cylinder'],
                           'J' : ['FRP',      'Complex'],
                           'K' : ['Assembly', 'Cylinder'],
                           'L' : ['FRP',      'Aerofoil'], 
                           'M' : ['FRP',      'Aerofoil'],
                           'N' : ['FRP',      'Aerofoil'],
                           'O' : ['Assembly', 'Assembly'],
                           'P' : ['Assembly', 'Assembly'],
                           '1' : ['Ground']}

    aeroplane2.joints = {'1':  [['A1','A2'], [34.2, 14.68, 5.165], 'Perfect'],
                         '2':  [['A2','A3'], [34.2, 60.96, 5.165], 'Perfect'],
                         '3':  [['A2','B'],  [32.2, 29.79, 2.89],  'Lug'],
                         '4':  [['B', 'C'],  [13.2, 42.67, 4.74],  'Complex'],
                         '5':  [['C', 'D'],  [13.2, 40.17, 4.74],  'Complex'],
                         '6':  [['B', 'E'],  [23.2, 30.79, 3.57],  'Complex'],
                         '7':  [['E', 'F'],  [23.2, 28.29, 3.57],  'Complex'],
                         '8':  [['A2','G'],  [36.2, 29.79, 2.89],  'Lug'],
                         '9':  [['G', 'H'],  [45.2, 30.79, 3.57],  'Complex'],
                         '10': [['H', 'I'],  [45.2, 28.29, 3.57],  'Complex'],
                         '11': [['G', 'J'],  [55.2, 42.67, 4.74],  'Complex'],
                         '12': [['J', 'K'],  [55.2, 40.17, 4.74],  'Complex'],
                         '13': [['A3','L'],  [33.2, 68.58, 7.55],  'Lug'],
                         '14': [['A3','M'],  [35.2, 68.58, 7.55],  'Lug'],
                         '15': [['A3','N'],  [34.2, 64.58, 9.16],  'Lug'],
                         '16': [['A1','O'],  [34.2, 7.75,  1.75],  'Complex'],
                         '17': [['A2','P'],  [34.2, 29.67, 1.75],  'Complex'],
                         '18': [['O', '1'],  [34.2, 7.75,  0],     'Friction'],
                         '19': [['P', '1'],  [34.2, 29.67, 0],     'Friction']}
    aeroplane2.addElements()
    aeroplane2.addJoints()
    aeroplane2.edgeList()

    print("Turbine nodes:", turbine1.nodes)
    print("Aeroplane nodes:", aeroplane1.nodes)
    
    # Generate the modular product graph
    V, E = network.modularProduct(turbine1, aeroplane1)
    print("Modular product edges:", len(E))
    print("Modular product vertices:", len(V))
    modularProduct = nx.Graph()
    modularProduct.add_nodes_from(V)
    modularProduct.add_edges_from(E)
    # nx.draw(modularProduct, with_labels=True)
    # plt.show()

    # Time the networkX algorithm
    # cliques = find_cliques(modularProduct)
    # Find the largest cliques

    E1 = turbine1.edgeList()
    E2 = aeroplane1.edgeList()
    
    cEdges, dEdges = network.findCedges(E, E1, E2)
    print("Number of c-edges:", len(cEdges))
    print("Number of d-edges:", len(dEdges))

    N = network.neighbourSet(V, E)
    total = sum([len(N[v]) for v in N])
    print("Size of neighbour set:", total)

    # cEdgeGraph = nx.Graph()
    # cEdgeGraph.add_edges_from(cEdges)
    # cEdgeGraph.add_nodes_from(V)

    # nx.draw(cEdgeGraph, with_labels=True)
    # plt.show()

    # c-clique algorithm (broken)

    start = time.time()
    cliques = list(network.maximalCliquesCedges(V, E, cEdges, dEdges))
    cliques = [set(item) for item in set(frozenset(item) for item in cliques)]
    c_cliques = check_adjacency(cliques, cEdges)
    max_cliques = maxCliques(cliques)
    end = time.time()

    # BK cliques (also broken)

    # start = time.time()
    # cliques_BK = network.maximalCliquesBK(V, E)
    # c_cliques = check_adjacency(cliques_BK, cEdges)
    # max_cliques = maxCliques(c_cliques)
    # end = time.time()

    """
    print("Largest cliques found using BK pivot")
    for i, clique in enumerate(max_cliques_BK):
        print("Max clique", i+1, ":", clique)

    print("Number of cliques:", len(cliques_BK))

    print("\n###################################\n")
    """
    # Cliques found using c-cliques
    for i, clique in enumerate(max_cliques):
        print("Max clique", i+1, ":", clique)

    print("Time to find:", end - start)
    print("Number of cliques:", len(c_cliques))

    # Found
    # Max clique 8 : {('H', 'K'), ('C', 'M'), ('D', 'A3'), ('E', 'A2'), ('F', 'G'), ('G', 'J'), ('B', 'N'), ('A', 'L')}
    # VERRRY BOTCHY code to produce the graph for the above subgraph, regardless of which cliques the subgraph matching algorithm finds

    # mcs = {('H', 'K'), ('C', 'M'), ('D', 'A3'), ('E', 'A2'), ('F', 'G'), ('G', 'J'), ('B', 'N'), ('A', 'L')}
    mcs = max_cliques[0]
    subgraph_edges = []
    for v1 in mcs:
        for v2 in mcs:
            if ((v1,v2) in cEdges) or ((v2,v1) in cEdges):
                subgraph_edges.append((v1,v2))
    
    subgraph = nx.Graph()
    subgraph.add_nodes_from(mcs)
    subgraph.add_edges_from(subgraph_edges)

    # Initiliase nx.Graph object
    turbine1Graph = nx.Graph()
    # Add nodes and edges from turbine1
    turbine1Graph.add_nodes_from(turbine1.nodeList())
    turbine1Graph.add_edges_from(turbine1.edgeList())

    # Initiliase nx.Graph object
    aeroplane1Graph = nx.Graph()
    # Add nodes and edges from aeroplane    
    aeroplane1Graph.add_nodes_from(aeroplane1.nodeList())
    aeroplane1Graph.add_edges_from(aeroplane1.edgeList())

    # Create subplots with bridge graphs
    plt.subplot(121)
    nx.draw(turbine1Graph, with_labels=True, pos=nx.spring_layout(turbine1Graph))
    plt.subplot(122)
    nx.draw(aeroplane1Graph, with_labels=True, pos=nx.spring_layout(aeroplane1Graph))
    plt.show()

    nx.draw(subgraph, with_labels=True)
    plt.show()