from structure import Structure
from structure import Network
from element import Boundary
from element import IrreducibleElement
from joint import Joint

import graph_comparison as gc
import backtracking as bt
import network as nw
import time

def plotBridgeMCS(MCS_nodes, graph1, graph2):
    MCS_edges = []
    for node1 in MCS_nodes:
        for node2 in MCS_nodes:
            if node1 != node2:
                v1 = node1[0]
                v2 = node2[0]
                u1 = node1[1]
                u2 = node2[1]
                if v2 in graph1[v1] and u2 in graph2[u1]:
                    MCS_edges.append((node1, node2))
    gc.graphPlot(MCS_nodes, MCS_edges)

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

    start_time = time.time()
    matches = bt.backtrack(graph1.graph, graph2.graph, 'bridges.txt')
    end_time = time.time()
    time_taken = end_time - start_time
    
    print("Time taken: {0} seconds".format(round(time_taken, 2)))
    print("Number of matches", len(matches))

    f=open('matches.txt','w')
    for match in matches:
        print(match)
        f.write('subgraphs/' + str(match) +'\n')
    f.write("Time taken: {0} seconds".format(round(time_taken, 2)))
    f.close()

    # MCS_nodes = [('X', 'DD'), ('Q', 'BB'), ('K', 'AA'), ('W', 'CC'), ('J', 'R'), ('L', 'F'), ('M', '1'), 
    #              ('N', 'S'), ('O', 'T'), ('P', 'U'), ('R', 'L'), ('S', 'V'), ('T', 'W'), ('U', 'X'), 
    #              ('V', 'Y'), ('D', 'Z'), ('F', 'N'), ('G', 'O'), ('H', 'P'), ('I', 'Q'), ('Z', 'EE'), 
    #              ('Y', 'FF')]

    # gc.plotMCSfromNodes(MCS_nodes, graph1.graph, graph2.graph)

    # distance = gc.createDistanceMatrix([randlestown, castledawson], "JaccardBackTrack")
    # print(distance)