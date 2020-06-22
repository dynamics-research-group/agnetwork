from structure import Structure
from structure import Network
from element import Boundary
from element import IrreducibleElement
from joint import Joint

import graph_comparison as gc
import backtracking as bt
import backtracking_parallel as btp
import network as nw
import networkx as nx
import time

if __name__ == '__main__':

    # Randlestown bridge

    randlestown = Structure('randlestown bridge')
    file_path = "IE_models/Randlestown_West_Deck_Bridge.xlsx"
    gc.importIE(randlestown, file_path)

    # Castledawson bridge

    castledawson = Structure('castledawson bridge')
    file_path = "IE_models/Castledawson_Bridge_IEM_revB.xlsx"
    gc.importIE(castledawson, file_path)

    
    graph1, graph2 = gc.smallestGraphFirst(castledawson, randlestown)

    # Re-generate node list
    V1 = graph1.nodeList()
    V2 = graph2.nodeList()
    # Generate edge list
    E1 = graph1.edgeList()
    E2 = graph2.edgeList()
    # # Plot the two graphs
    # gc.graphPlot(V1, E1)
    # gc.graphPlot(V2, E2)

    # start_time = time.time()
    # matches = btp.backtrackParallel(graph1.graph, graph2.graph, 'bridges.txt')
    # end_time = time.time()
    # time_taken = end_time - start_time
    
    # print("Time taken: {0} seconds".format(round(time_taken, 2)))
    # print("Number of matches", len(matches))

    # with open('matches.txt','w') as f:
    #     for match in matches:
    #         print(match)
    #         f.write('subgraphs/' + str(match) +'\n')
    #     f.write("Time taken: {0} seconds".format(round(time_taken, 2)))

    # MCS_nodes = [('X', 'DD'), ('Q', 'BB'), ('K', 'AA'), ('W', 'CC'), ('J', 'R'), ('L', 'F'), ('M', '1'), 
    #              ('N', 'S'), ('O', 'T'), ('P', 'U'), ('R', 'L'), ('S', 'V'), ('T', 'W'), ('U', 'X'), 
    #              ('V', 'Y'), ('D', 'Z'), ('F', 'N'), ('G', 'O'), ('H', 'P'), ('I', 'Q'), ('Z', 'EE'), 
    #              ('Y', 'FF')]

    MCS_nodes = [('X', 'DD'), ('Q', 'BB'), ('K', 'AA'), ('W', 'CC'), ('E', 'M'), ('J', 'R'), ('L', 'S'), ('M', 'T'), ('N', 'U'), ('O', 'V'), ('R', 'W'), ('S', 'X'), ('T', 'Y'), ('U', 'Z'), ('A', 'B'), ('B', 'F'), ('C', 'H'), ('D', 'L'), ('F', 'N'), ('G', 'O'), ('H', 'P'), ('I', 'Q'), ('Z', 'EE'), ('Y', 'FF')]

    nodes, edges = gc.plotMCSfromNodes(MCS_nodes, graph1.graph, graph2.graph)

    # Create new networkX graph object
    G = nx.Graph()
    # Add nodes and edges to the graph object
    G.add_edges_from(edges)
    G.add_nodes_from(nodes)

    nx.write_pajek(G, "test.net")

    G1 = nx.Graph()
    G1.add_edges_from(edges)
    G1.add_nodes_from(nodes)

    nx.write_pajek(G1, "test.net")

    # distance = gc.createDistanceMatrix([randlestown, castledawson], "JaccardBackTrack")
    # print(distance)