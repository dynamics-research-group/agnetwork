from structure import Structure
from structure import Network
from element import Boundary
from element import IrreducibleElement
from joint import Joint

import graph_comparison as gc
import network as nw
import pandas as pd
import time

if __name__ == '__main__':

    # Randlestown bridge

    elements = pd.read_excel (r"IE_models/Randlestown_West_Deck_Bridge.xlsx", sheet_name='Elements', usecols="A:I")
    joints = pd.read_excel (r"IE_models/Randlestown_West_Deck_Bridge.xlsx", sheet_name='Joints', usecols="A:H")
    boundary_conditions = pd.read_excel (r"IE_models/Randlestown_West_Deck_Bridge.xlsx", sheet_name='Boundary conditions', usecols="A:C")

    randlestown = Structure('randlestown bridge')
    boundary_list = [str(bc) for bc in boundary_conditions['Element ID']]
    element_list = list(elements['Element ID']) + boundary_list
    randlestown.elements = dict.fromkeys(element_list)

    joint_keys = [tuple(joint.split(', ')) for joint in joints['Joint set']]
    joint_values = [[str(i),[],''] for i in range(1, len(joint_keys)+1)]
    randlestown.joints = dict(zip(joint_keys, joint_values))
    for joint in randlestown.joints:
        print(joint)

    randlestown.addElements()
    randlestown.addJoints()
    randlestown.edgeList()

    # Castledawson bridge

    elements = pd.read_excel (r"IE_models/Castledawson_Bridge_IEM_revB.xlsx", sheet_name='Elements', usecols="A:I")
    joints = pd.read_excel (r"IE_models/Castledawson_Bridge_IEM_revB.xlsx", sheet_name='Joints', usecols="A:H")
    boundary_conditions = pd.read_excel (r"IE_models/Castledawson_Bridge_IEM_revB.xlsx", sheet_name='Boundary conditions', usecols="A:C")

    castledawson = Structure('castledawson bridge')
    boundary_list = [str(bc) for bc in boundary_conditions['Element ID']]
    element_list = list(elements['Element ID']) + boundary_list
    castledawson.elements = dict.fromkeys(element_list)
    
    joint_keys = [tuple(joint.split(', ')) for joint in joints['Joint set']]
    joint_values = [[str(i),[],''] for i in range(1, len(joint_keys)+1)]
    castledawson.joints = dict(zip(joint_keys, joint_values))
    for joint in castledawson.joints:
        print(joint)

    castledawson.addElements()
    castledawson.addJoints()
    castledawson.edgeList()

    begin_time = time.time()
    distance = gc.findJaccardDistance(randlestown, castledawson, plot=True)
    end_time = time.time()
    print("Time taken:", round(end_time - begin_time, 2), "seconds")