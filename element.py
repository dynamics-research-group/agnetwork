from structure import Structure

class Element(Structure):
    # Create an instance of elements with user-defined ID and default attributes
    def __init__(self,
                 elementID):
        self.elementID = elementID
        Element.elements[elementID] = []
    
    def remove(self):
        try:
            del Element.elements[self.elementID]
        except:
            return None

class Beam(Element):
    def __init__(self,
                 beamID,
                 length=1,
                 mass=1):
        Element.__init__(self, beamID)
        self.length = length
        self.mass = mass
        Element.elements[beamID] = [mass, length]

class Boundary(Element):
    # Create an instance of a boundary condition with user-defined ID and default attributes
    def __init__(self,
                 boundaryID,
                 disp=0,
                 trac=0):
        Element.__init__(self, boundaryID)
        self.disp = disp
        self.trac = trac
        Element.elements[boundaryID] = [disp, trac]