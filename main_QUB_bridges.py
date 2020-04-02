from structure import Structure
from structure import Network
from element import Boundary
from element import IrreducibleElement
from joint import Joint

import graph_comparison as gc
import network as nw
import pandas as pd

if __name__ == '__main__':

    # Randlestown bridge

    elements = pd.read_excel (r"IE_models/Randlestown_West_Deck_Bridge.xlsx", sheet_name='Elements', usecols="A:I")
    joints = pd.read_excel (r"IE_models/Randlestown_West_Deck_Bridge.xlsx", sheet_name='Joints', usecols="A:H")
    boundary_conditions = pd.read_excel (r"IE_models/Randlestown_West_Deck_Bridge.xlsx", sheet_name='Boundary conditions', usecols="A:C")

    randlestown = Structure('randlestown bridge')
    boundary_list = [str(bc) for bc in boundary_conditions['Element ID']]
    element_list = list(elements['Element ID']) + boundary_list
    randlestown.elements = dict.fromkeys(element_list)

    joint_keys = [(joint[0], joint[-1]) for joint in joints['Joint set']]
    joint_values = [[str(i),[],''] for i in range(1, len(joint_keys))]
    randlestown.joints = dict(zip(joint_keys, joint_values))

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

    joint_keys = [(joint[0], joint[-1]) for joint in joints['Joint set']]
    joint_values = [[str(i),[],''] for i in range(1, len(joint_keys))]
    castledawson.joints = dict(zip(joint_keys, joint_values))

    castledawson.addElements()
    castledawson.addJoints()
    castledawson.edgeList()

    distance = gc.findJaccardDistance(randlestown, castledawson, plot=True)
