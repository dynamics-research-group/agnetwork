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

    begin_time = time.time()
    distance = gc.findJaccardDistance(randlestown, castledawson)
    end_time = time.time()
    print("Time taken:", round(end_time - begin_time, 2), "seconds")