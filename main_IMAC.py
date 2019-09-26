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
import maximal_cliques as mc
import graph_comparison as gc

divide = "\n###################################\n"

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
    aeroplane1 = Structure('Boeing-747')
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
    aeroplane2 = Structure('Cessna-172')
    aeroplane2.elements = {'A' : ['Aluminium',  'Aerofoil'],
                           'B' : ['Aluminium',  'Aerofoil'],
                           'C' : ['Aluminium',  'Complex'],
                           'D1': ['FRP',        'Rectangular shell'], 
                           'D2': ['Mixed',      'Trapezoid'],
                           'D3': ['FRP',        'Trapezoid'],
                           'E' : ['FRP',        'Aerofoil'],
                           'F' : ['FRP',        'Aerofoil'],
                           'G' : ['Aluminium',  'Cylindrical beam'],
                           'H' : ['Aluminium',  'Cylindrical beam'],
                           'I' : ['FRP',        'Aerofoil'],
                           'J' : ['FRP',        'Aerofoil'],
                           'K' : ['FRP',        'Aerofoil'],
                           'L' : ['Assembly',   'Assembly'], 
                           'M' : ['Assembly',   'Assembly'],
                           '1' : ['Ground']}

    aeroplane2.joints = {'1':  [['A', 'C'],   [0, 0, 0], 'Bolted'],
                         '2':  [['B', 'C'],   [0, 0, 0], 'Bolted'],
                         '3':  [['C', 'D1'],  [0, 0, 0], 'Lug'],
                         '4':  [['D1', 'D2'], [0, 0, 0], 'Perfect'],
                         '5':  [['D1', 'D3'], [0, 0, 0], 'Perfect'],
                         '6':  [['E', 'D2'],  [0, 0, 0], 'Complex'],
                         '7':  [['F', 'D2'],  [0, 0, 0], 'Complex'],
                         '8':  [['D3', 'I'],  [0, 0, 0], 'Lug'],
                         '9':  [['D3', 'J'],  [0, 0, 0], 'Complex'],
                         '10': [['D3', 'K'],  [0, 0, 0], 'Complex'],
                         '11': [['D1', 'L'],  [0, 0, 0], 'Complex'],
                         '12': [['D1', 'M'],  [0, 0, 0], 'Complex'],
                         '13': [['D1', 'G'],  [0, 0, 0], 'Pinned'],
                         '14': [['D1', 'H'],  [0, 0, 0], 'Pinned'],
                         '15': [['E', 'G'],   [0, 0, 0], 'Pinned'],
                         '16': [['F', 'H'],   [0, 0, 0], 'Pinned'],
                         '17': [['L', '1'],   [0, 0, 0], 'Friction'],
                         '18': [['M', '1'],   [0, 0, 0], 'Friction']}
    
    aeroplane2.addElements()
    aeroplane2.addJoints()
    aeroplane2.edgeList()

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

    graph1 = bridge3
    graph2 = aeroplane2
    
    print("Turbine nodes:", graph1.nodes)
    print("Aeroplane nodes:", graph2.nodes)
    print(divide)
    
    # Generate the modular product graph
    V, E = gc.modularProduct(graph1, graph2)
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

    V1 = graph1.nodeList()
    V2 = graph2.nodeList()
    E1 = graph1.edgeList()
    E2 = graph2.edgeList()
    
    cEdges, dEdges = gc.findCedges(E, E1, E2)
    print("Number of c-edges:", len(cEdges))
    print("Number of d-edges:", len(dEdges))

    N = gc.neighbourSet(V, E)
    total = sum([len(N[v]) for v in N])
    print("Size of neighbour set:", total)
    print(divide)

    cEdgeGraph = nx.Graph()
    cEdgeGraph.add_edges_from(cEdges)
    cEdgeGraph.add_nodes_from(V)

    # nx.draw(cEdgeGraph, with_labels=True)
    # plt.show()

    # c-clique algorithm (broken)

    start = time.time()
    print("Finding cliques...")
    cliques = list(gc.maximalCliquesCedges(V, E, cEdges, dEdges))
    print("Removing duplicates...")
    cliques = [set(item) for item in set(frozenset(item) for item in cliques)]
    print("Checking cliques for adjacency...")
    c_cliques = gc.check_adjacency(cliques, cEdges)
    print("Finding largest cliques...")
    max_cliques = gc.maxCliques(c_cliques)
    end = time.time()
    print(divide)

    # BK cliques (misses 8-clique with degree 3, 'The Cross')

    # start = time.time()
    # print("Finding cliques...")
    # cliques_BK = network.maximalCliquesBK(V, E)
    # print("Checking cliques for adjacency...")
    # c_cliques = check_adjacency(cliques_BK, cEdges)
    # print("Finding largest cliques...")
    # max_cliques = maxCliques(c_cliques)
    # end = time.time()
    # print(divide)

    # Maximal cliques (downloaded)

    # start = time.time()
    # print("Create graph...")
    # G = network.neighbourSet(V, E)
    # print("Finding cliques...")
    # cliques = mc.find_cliques(G)
    # print("Checking cliques for adjacency...")
    # c_cliques = check_adjacency(cliques, cEdges)
    # print("Finding largest cliques...")
    # max_cliques = maxCliques(c_cliques)
    # end = time.time()
    # print(divide)
    
    # Cliques found using c-cliques
    for i, clique in enumerate(max_cliques):
        print("Max clique", i+1, ":", clique)
    print(divide)

    print("Time to find:", round(end - start, 2), "seconds")
    print("Number of c-cliques:", len(c_cliques))
    try:
        print("Number of cliques:", len(cliques_BK))
        print("The Cross?", {('H', 'K'), ('C', 'M'), ('D', 'A3'), ('E', 'A2'), ('F', 'G'), ('G', 'J'), ('B', 'N'), ('A', 'L')} in cliques_BK)
    except:
        print("Number of cliques:", len(cliques))
        print("The Cross?", {('H', 'K'), ('C', 'M'), ('D', 'A3'), ('E', 'A2'), ('F', 'G'), ('G', 'J'), ('B', 'N'), ('A', 'L')} in cliques)

    ss = gc.mcsSimilarityScore(max_cliques[0], V1, V2)
    print("Similarity score:", round(ss, 2) , "%")

    # mcs = {('H', 'K'), ('C', 'M'), ('D', 'A3'), ('E', 'A2'), ('F', 'G'), ('G', 'J'), ('B', 'N'), ('A', 'L')}

    # Initiliase nx.Graph object
    graph1nx = nx.Graph()
    # Add nodes and edges from graph1
    graph1nx.add_nodes_from(graph1.nodeList())
    graph1nx.add_edges_from(graph1.edgeList())

    # Initiliase nx.Graph object
    graph2nx = nx.Graph()
    # Add nodes and edges from graph2   
    graph2nx.add_nodes_from(graph2.nodeList())
    graph2nx.add_edges_from(graph2.edgeList())

    # Create subplots with bridge graphs
    plt.subplot(121)
    nx.draw(graph1nx, with_labels=True, pos=nx.spring_layout(graph1nx))
    plt.subplot(122)
    nx.draw(graph2nx, with_labels=True, pos=nx.spring_layout(graph2nx))
    plt.show()

    mcs = max_cliques[0]
    subgraph_edges = []
    for v1 in mcs:
        for v2 in mcs:
            if ((v1,v2) in cEdges) or ((v2,v1) in cEdges):
                subgraph_edges.append((v1,v2))
    
    subgraph = nx.Graph()
    subgraph.add_nodes_from(mcs)
    subgraph.add_edges_from(subgraph_edges)

    nx.draw(subgraph, with_labels=True)
    plt.show()