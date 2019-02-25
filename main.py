from structure import Structure
from element import Boundary
from element import Beam
from joint import Joint

if __name__ == '__main__':
    Struct1 = Structure("Car")
    lenA = 5
    lenB = 5
    BC1 = Boundary(1)
    BeamA = Beam('A')
    BeamB = Beam('B')
    BC2 = Boundary(2)
    BC3 = Boundary(3)
    J1 = Joint(1, [1, 'A'], [0, lenB])
    J2 = Joint(2, ['B', 'A'], [lenA/2, lenB])
    J3 = Joint(3, [2, 'B'], [lenA/2, 0])
    J4 = Joint(4, [3, 'A'], [lenA, lenB])
    print(Struct1.joints)
    print(Struct1.elements)
    Struct1.addElements()
    Struct1.addJoints()
    print(Struct1.graph)