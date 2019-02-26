from structure import Structure
from element import Boundary
from element import Beam
from joint import Joint

if __name__ == '__main__':
    turbine = Structure('Turbine')
    bridge = Structure('Bridge')
    len_a = 5
    len_b = 5

    # Specify the car
    turbine_bc1 = Boundary(1, 'Turbine')
    turbine_beam_a = Beam('A', 'Turbine')
    turbine_beam_b = Beam('B', 'Turbine')
    turbine_j1 = Joint(1, [1, 'A'], [0, 0], 'Turbine')
    turbine_j2 = Joint(2, ['A', 'B'], [0, len_a], 'Turbine')

    # Specify the bridge
    bridge_bc1 = Boundary(1,'Bridge')
    bridge_bc2 = Boundary(2, 'Bridge')
    bridge_bc3 = Boundary(3, 'Bridge')
    bridge_beam_a = Beam('A', 'Bridge')
    bridge_beam_b = Beam('B', 'Bridge')
    bridge_j1 = Joint(1, [1, 'A'], [0, len_b], 'Bridge')
    bridge_j2 = Joint(2, ['B', 'A'], [len_a/2, len_b], 'Bridge')
    bridge_j3 = Joint(3, [2, 'B'], [len_a/2, 0], 'Bridge')
    bridge_j4 = Joint(4, [3, 'A'], [len_a, len_b], 'Bridge')
    
    print(Structure.elements)
    print(Structure.joints)
    bridge.addElements()
    bridge.addJoints()
    print(bridge.graph)
    turbine.addElements()
    turbine.addJoints()
    print(turbine.graph)