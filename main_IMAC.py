from structure import Structure
from structure import Network
from element import Boundary
from element import IrreducibleElement
from joint import Joint
import cProfile
import pstats

import graph_comparison as gc
import backtracking as bt
import network as nw
import pandas as pd
import time

if __name__ == '__main__':
    '''This code creates the attributed graph for two
    separate structures and performs a similarity
    comparison between them. This work will go into
    the IMAC paper.'''
    # network = Network()

    # Define the graph for a turbine
    turbine1 = Structure('Turbine1')
    turbine1.elements = {'A': ['FRP',      ['Beam', 'Aerofoil']], 
                         'B': ['FRP',      ['Beam', 'Aerofoil']],
                         'C': ['FRP',      ['Beam', 'Aerofoil']],
                         'D': ['FRP',      ['Complex', 'Rotor hub']],
                         'E': ['FRP',      ['Shell', 'Cuboid']],
                         'F': ['Metal',    ['Beam', 'Cylindrical']],
                         'G': ['Metal',    ['Beam', 'Cylindrical']],
                         'H': ['Metal',    ['Beam', 'Cylindrical']],
                         'I': ['Concrete', ['Plate', 'Cylindrical']],
                         '1': ['Ground']}                
    turbine1.joints = {('A','D') : ['1', [8, 15, 235.75], 'Bearing', ['x','y','z'], ['y','z']],
                       ('B','D') : ['2', [8, 14, 254],    'Bearing', ['x','y','z'], ['y','z']],
                       ('C','D') : ['3', [8, 16, 254],    'Bearing', ['x','y','z'], ['y','z']],
                       ('D','E') : ['4', [10, 15, 253],   'Bearing', ['x','y','z'], ['x','y']],
                       ('E','F') : ['5', [15, 15, 250],   'Bearing', ['x','y','z'], ['x','y']],
                       ('F','G') : ['6', [15, 15, 183],   'Bolted'],
                       ('G','H') : ['7', [15, 15, 105],   'Bolted'],
                       ('H','I') : ['8', [15, 15, 5],     'Bolted'],
                       ('I','1') : ['9', [15, 15, 0],     'Boundary']}
    turbine1.addElements()
    turbine1.addJoints()
    turbine1.edgeList()

    # Define the graph for an 747
    aeroplane1 = Structure('Boeing-747')
    aeroplane1.elements = {'A1': ['FRP',      ['Shell', 'Truncated cone']],
                           'A2': ['FRP',      ['Beam', 'Cylindrical']],
                           'A3': ['FRP',      ['Shell', 'Cone']],
                           'B' : ['FRP',      ['Beam', 'Aerofoil']], 
                           'C' : ['FRP',      ['Complex', 'Pylon']],
                           'D' : ['Assembly', ['Shell', 'Cylinder']],
                           'E' : ['FRP',      ['Complex', 'Pylon']],
                           'F' : ['Assembly', ['Shell', 'Cylinder']],
                           'G' : ['FRP',      ['Beam', 'Aerofoil']],
                           'H' : ['FRP',      ['Complex', 'Pylon']],
                           'I' : ['Assembly', ['Shell', 'Cylinder']],
                           'J' : ['FRP',      ['Complex', 'Pylon']],
                           'K' : ['Assembly', ['Shell', 'Cylinder']],
                           'L' : ['FRP',      ['Beam', 'Aerofoil']], 
                           'M' : ['FRP',      ['Beam', 'Aerofoil']],
                           'N' : ['FRP',      ['Beam', 'Aerofoil']],
                           'O' : ['Mixed',    ['Complex', 'Assembly']],
                           'P' : ['Mixed',    ['Complex', 'Assembly']],
                           '1' : ['Ground']}
    aeroplane1.joints = {('A1','A2') : ['1',  [34.2, 14.68, 5.165], 'Perfect'],
                         ('A2','A3') : ['2',  [34.2, 60.96, 5.165], 'Perfect'],
                         ('A2','B')  : ['3',  [32.2, 29.79, 2.89],  'Lug'],
                         ('B', 'C')  : ['4',  [13.2, 42.67, 4.74],  'Complex'],
                         ('C', 'D')  : ['5',  [13.2, 40.17, 4.74],  'Complex'],
                         ('B', 'E')  : ['6',  [23.2, 30.79, 3.57],  'Complex'],
                         ('E', 'F')  : ['7',  [23.2, 28.29, 3.57],  'Complex'],
                         ('A2','G')  : ['8',  [36.2, 29.79, 2.89],  'Lug'],
                         ('G', 'H')  : ['9',  [45.2, 30.79, 3.57],  'Complex'],
                         ('H', 'I')  : ['10', [45.2, 28.29, 3.57],  'Complex'],
                         ('G', 'J')  : ['11', [55.2, 42.67, 4.74],  'Complex'],
                         ('J', 'K')  : ['12', [55.2, 40.17, 4.74],  'Complex'],
                         ('A3','L')  : ['13', [33.2, 68.58, 7.55],  'Lug'],
                         ('A3','M')  : ['14', [35.2, 68.58, 7.55],  'Lug'],
                         ('A3','N')  : ['15', [34.2, 64.58, 9.16],  'Lug'],
                         ('A1','O')  : ['16', [34.2, 7.75,  1.75],  'Complex'],
                         ('A2','P')  : ['17', [34.2, 29.67, 1.75],  'Complex'],
                         ('O', '1')  : ['18', [34.2, 7.75,  0],     'Friction'],
                         ('P', '1')  : ['19', [34.2, 29.67, 0],     'Friction']}
    aeroplane1.addElements()
    aeroplane1.addJoints()
    aeroplane1.edgeList()

    # Define the graph for a Cessna 172
    aeroplane2 = Structure('Cessna-172')
    aeroplane2.elements = {'A' : ['Aluminium',  ['Beam', 'Aerofoil']],
                           'B' : ['Aluminium',  ['Beam', 'Aerofoil']],
                           'C' : ['Aluminium',  ['Complex', 'Rotor hub']],
                           'D1': ['FRP',        ['Shell', 'Rectangular']], 
                           'D2': ['Mixed',      ['Sehll', 'Trapezoid']],
                           'D3': ['FRP',        ['Sehll', 'Trapezoid']],
                           'E' : ['FRP',        ['Beam', 'Aerofoil']],
                           'F' : ['FRP',        ['Beam', 'Aerofoil']],
                           'G' : ['Aluminium',  ['Beam', 'Cylindrical']],
                           'H' : ['Aluminium',  ['Beam', 'Cylindrical']],
                           'I' : ['FRP',        ['Beam', 'Aerofoil']],
                           'J' : ['FRP',        ['Beam', 'Aerofoil']],
                           'K' : ['FRP',        ['Beam', 'Aerofoil']],
                           'L' : ['Mixed',      ['Complex', 'Assembly']], 
                           'M' : ['Mixed',      ['Complex', 'Assembly']],
                           '1' : ['Ground']}
    aeroplane2.joints = {('A', 'C')  : ['1',  [0, 0, 0], 'Bolted'],
                         ('B', 'C')  : ['2',  [0, 0, 0], 'Bolted'],
                         ('C', 'D1') : ['3',  [0, 0, 0], 'Lug'],
                         ('D1','D2') : ['4',  [0, 0, 0], 'Perfect'],
                         ('D1','D3') : ['5',  [0, 0, 0], 'Perfect'],
                         ('E', 'D2') : ['6',  [0, 0, 0], 'Complex'],
                         ('F', 'D2') : ['7',  [0, 0, 0], 'Complex'],
                         ('D3', 'I') : ['8',  [0, 0, 0], 'Lug'],
                         ('D3', 'J') : ['9',  [0, 0, 0], 'Complex'],
                         ('D3', 'K') : ['10', [0, 0, 0], 'Complex'],
                         ('D1', 'L') : ['11', [0, 0, 0], 'Complex'],
                         ('D1', 'M') : ['12', [0, 0, 0], 'Complex'],
                         ('D1', 'G') : ['13', [0, 0, 0], 'Pinned'],
                         ('D1', 'H') : ['14', [0, 0, 0], 'Pinned'],
                         ('E', 'G')  : ['15', [0, 0, 0], 'Pinned'],
                         ('F', 'H')  : ['16', [0, 0, 0], 'Pinned'],
                         ('L', '1')  : ['17', [0, 0, 0], 'Boundary'],
                         ('M', '1')  : ['18', [0, 0, 0], 'Boundary']}
    aeroplane2.addElements()
    aeroplane2.addJoints()
    aeroplane2.edgeList()

    # Define the graph for Bridge 1
    bridge1 = Structure('Bridge1')
    bridge1.elements = {'1' : ['Ground'],
                        '2' : ['Ground'],
                        '3' : ['Ground'], 
                        'A' : ['Concrete', 'Beam'], 
                        'B' : ['Concrete', 'Beam']}
    bridge1.joints = {('1','A') : ['1', [0, 0, 0], 'Simply supported'],
                      ('3','A') : ['2', [0, 0, 0], 'Simply supported'],
                      ('2','B') : ['3', [0, 0, 0], 'Clamped'],
                      ('A','B') : ['4', [0, 0, 0], 'Joined']}
    bridge1.addElements()
    bridge1.addJoints()
    bridge1.edgeList()

    # Define the graph for Bridge 2
    bridge2 = Structure('Bridge2')
    bridge2.elements = {'1' : ['Ground'],
                        '2' : ['Ground'],
                        '3' : ['Ground'], 
                        '4' : ['Ground'],
                        'A' : ['Concrete', 'Beam'], 
                        'B' : ['Concrete', 'Beam'],
                        'C' : ['Concrete', 'Beam'], 
                        'D' : ['Concrete', 'Beam']}
    bridge2.joints = {('1','A') : ['1', [0, 0, 0], 'Simply supported'],
                      ('4','C') : ['2', [0, 0, 0], 'Simply supported'],
                      ('2','B') : ['3', [0, 0, 0], 'Clamped'],
                      ('3','D') : ['4', [0, 0, 0], 'Clamped'],
                      ('A','B') : ['5', [0, 0, 0], 'Joined'],
                      ('A','C') : ['6', [0, 0, 0], 'Joined'],
                      ('C','D') : ['7', [0, 0, 0], 'Joined']}
    bridge2.addElements()
    bridge2.addJoints()
    bridge2.edgeList()

    # Define the graph for Bridge 2a
    bridge2a = Structure('Bridge2a')
    bridge2a.elements = {'1' : ['Ground'],
                        '2' : ['Ground'],
                        '3' : ['Ground'], 
                        '4' : ['Ground'],
                        'A' : ['Concrete', 'Beam'], 
                        'B' : ['Concrete', 'Beam'],
                        'C' : ['Concrete', 'Beam'], 
                        'D' : ['Concrete', 'Beam']}
    bridge2a.joints = {('1','A') : ['1', [0, 0, 0], 'Simply supported'],
                      ('4','C') : ['2', [0, 0, 0], 'Simply supported'],
                      ('2','B') : ['3', [0, 0, 0], 'Clamped'],
                      ('3','D') : ['4', [0, 0, 0], 'Clamped'],
                      ('A','B') : ['5', [0, 0, 0], 'Joined'],
                      ('A','C') : ['6', [0, 0, 0], 'Joined'],
                      ('C','D') : ['7', [0, 0, 0], 'Joined']}
    bridge2a.addElements()
    bridge2a.addJoints()
    bridge2a.edgeList()

    # Define the graph for Bridge 3
    bridge3 = Structure('Bridge3')
    bridge3.elements = {'1' : ['Ground'],
                        '2' : ['Ground'],
                        '3' : ['Ground'], 
                        '4' : ['Ground'],
                        '5' : ['Ground'],
                        'A' : ['Concrete', 'Beam'], 
                        'B' : ['Concrete', 'Beam'],
                        'C' : ['Concrete', 'Beam'], 
                        'D' : ['Concrete', 'Beam'],
                        'E' : ['Concrete', 'Beam'],
                        'F' : ['Concrete', 'Beam']}
    bridge3.joints = {('1','A') : ['1',  [0, 0, 0], 'Simply supported'],
                      ('5','E') : ['2',  [0, 0, 0], 'Simply supported'],
                      ('2','B') : ['3',  [0, 0, 0], 'Clamped'],
                      ('3','D') : ['4',  [0, 0, 0], 'Clamped'],
                      ('4','F') : ['5',  [0, 0, 0], 'Clamped'],
                      ('A','B') : ['6',  [0, 0, 0], 'Joined'],
                      ('A','C') : ['7',  [0, 0, 0], 'Joined'],
                      ('C','D') : ['8',  [0, 0, 0], 'Joined'],
                      ('C','E') : ['9',  [0, 0, 0], 'Joined'],
                      ('E','F') : ['10', [0, 0, 0], 'Joined']}
    bridge3.addElements()
    bridge3.addJoints()
    bridge3.edgeList()

    graph_list = [turbine1, bridge1, bridge2, bridge2a]
    graph_list2 = [aeroplane1, aeroplane2]

    # distance = gc.findJaccardDistanceBK(turbine1, aeroplane2, BCmatch=False, plot=True)
    
    # distance_matrix_BK = gc.createDistanceMatrix(graph_list + graph_list2, "JaccardBK")

    # print(distance_matrix_BK)

    # [[0.         0.5        0.5        0.5        0.61904762 0.63157895]
    # [0.5        0.         0.375      0.375      0.73684211 0.6875    ]
    # [0.5        0.375      0.         0.         0.57894737 0.58823529]
    # [0.5        0.375      0.         0.         0.57894737 0.58823529]
    # [0.61904762 0.73684211 0.57894737 0.57894737 0.         0.40909091]
    # [0.63157895 0.6875     0.58823529 0.58823529 0.40909091 0.        ]]

    # distance = gc.findJaccardDistanceBackTrack(turbine1, aeroplane2)
    # print(distance)

    distance_matrix_backtrack = gc.createDistanceMatrix(graph_list + graph_list2, "JaccardBackTrack")
    print(distance_matrix_backtrack)

    # graph1, graph2 = gc.smallestGraphFirst(graph_list[0], graph_list[2])
    # matches = bt.backtrack(graph1.graph, graph2.graph, 'IMAC.txt')
    # MCS_nodes = matches[-1]

    # gc.plotMCSfromNodes(MCS_nodes, graph1.graph, graph2.graph)

    # Largest graph first
    # [[0.         0.5        0.5        0.5        0.61904762 0.55555556]
    # [0.5        0.         0.375      0.375      0.73684211 0.6875    ]
    # [0.5        0.375      0.         0.         0.57894737 0.5       ]
    # [0.5        0.375      0.         0.         0.57894737 0.5       ]
    # [0.61904762 0.73684211 0.57894737 0.57894737 0.         0.15789474]
    # [0.55555556 0.6875     0.5        0.5        0.15789474 0.        ]]

    # Smallest graph first
    # [[0.         0.5        0.5        0.5        0.55       0.375     ]
    # [0.5        0.         0.375      0.375      0.73684211 0.6875    ]
    # [0.5        0.375      0.         0.         0.57894737 0.5       ]
    # [0.5        0.375      0.         0.         0.57894737 0.5       ]
    # [0.55       0.73684211 0.57894737 0.57894737 0.         0.15789474]
    # [0.375      0.6875     0.5        0.5        0.15789474 0.        ]]

    # Induced graph heuristic
    # [[0.         0.5        0.5        0.5        0.55       0.47058824]
    # [0.5        0.         0.375      0.375      0.73684211 0.6875    ]
    # [0.5        0.375      0.         0.         0.57894737 0.58823529]
    # [0.5        0.375      0.         0.         0.57894737 0.58823529]
    # [0.55       0.73684211 0.57894737 0.57894737 0.         0.25      ]
    # [0.47058824 0.6875     0.58823529 0.58823529 0.25       0.        ]]

    # profile = cProfile.Profile()
    # # profile.runcall(gc.createDistanceMatrix, graph_list + graph_list2, "JaccardBackTrack")
    # profile.runcall(bt.backtrack, graph_list2[1].graph, graph_list2[0].graph, 'IMAC.txt')
    # ps = pstats.Stats(profile)
    # ps.print_stats()
    # filename = 'profiles/main_IMAC.prof'  # You can change this if needed
    # profile.dump_stats(filename)

    """
    # Create initial weights matrix
    weights = nw.initWeightsDict(graph_list)
    # Create and print initial dataframe
    graph_strings = [str(graph) for graph in graph_list]
    network_weights = pd.DataFrame(data=weights, index=weights.keys())
    print("Initial weights:")
    print(network_weights)
    print()

    # Update the weights based on size of the graphs
    weights = nw.updateWeights(weights,1)
        
    # Create and print a new dataframe using the updated weights
    network_weights = pd.DataFrame(data=weights, index=weights.keys())
    print("Final weights:")
    print(network_weights)
    print()

    # Add bridge3 to weights
    weights = nw.addNewGraph(aeroplane1, weights)
    weights = nw.addNewGraph(bridge3, weights)
    weights = nw.addNewGraph(aeroplane2, weights)
    # Update the weights again
    weights = nw.updateWeights(weights,5)

    network_weights = pd.DataFrame(data=weights, index=weights.keys())
    
    print("New weights:")
    print(network_weights)
    print()

    # # Generate a similarity score based on the element and joint attributes
    # max_cliques_with_ss = ss.attributeSimilarityScore(max_cliques, cEdges, graph1, graph2)
    # for clique in max_cliques_with_ss[:50]:
    #     print(clique[0], "Element:", round(clique[1], 2), "Joint:", round(clique[2], 2))
    """