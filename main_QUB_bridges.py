from structure import Structure
from structure import Network
from element import Boundary
from element import IrreducibleElement
from joint import Joint

import graph_comparison as gc
import network as nw
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

    start_time = time.time()
    matches = gc.backtrack(graph1.graph, graph2.graph, 'bridges.txt')
    end_time = time.time()
    time_taken = end_time - start_time
    
    print("Time taken: {0} seconds".format(round(time_taken, 2)))
    print("Number of matches", len(matches))

    f=open('matches.txt','w')
    for match in matches:
        print(match)
        f.write(str(match)+'\n')
    f.write("Time taken: {0} seconds".format(round(time_taken, 2)))
    f.close()

    # distance = gc.createDistanceMatrix([randlestown, castledawson], "JaccardBackTrack")
    # print(distance)