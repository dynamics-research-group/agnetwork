from structure import Structure
from structure import Network
from element import Boundary
from element import IrreducibleElement
from joint import Joint
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':
    '''This code creates the attributed graph for two
    separate structures and performs a similarity
    comparison between them.'''
    # Define the graph for a turbine
    turbine1 = Structure('Turbine')
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

    # Define the graph for an aeroplane
    aeroplane1 = Structure('Aeroplane')
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
    nx.draw(turbine1Graph, with_labels=True)
    plt.subplot(122)
    nx.draw(aeroplane1Graph, with_labels=True)
    plt.show()