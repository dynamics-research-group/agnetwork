from structure import Structure

class Element(Structure):
    """Create an instance of elements with user-defined ID"""
    def __init__(self,
                 elementID):
        self.elementID = elementID
        Element.elements[elementID] = []
    
    def remove(self):
        """Removes the dictionary entry for the elements"""
        try:
            del Element.elements[self.elementID]
        except:
            return None
    
    def removeConnections(self):
        """Removes any joints connected to the element"""
        for jointID in list(Element.joints.keys()):
            localJoint = Element.joints[jointID][0]
            if self.elementID in localJoint:
                del Element.joints[jointID]
    
    def __del__(self):
        self.removeConnections()
        self.remove()

class Beam(Element):
    """Create a beam element with default attributes"""
    def __init__(self,
                 elementID,
                 length=1,
                 mass=1):
        Element.__init__(self, elementID)
        self.length = length
        self.mass = mass
        Element.elements[elementID] = [mass, length]

class Boundary(Element):
    """Create a boundary condition with default attributes"""
    def __init__(self,
                 elementID,
                 disp=0,
                 trac=0):
        Element.__init__(self, elementID)
        self.disp = disp
        self.trac = trac
        Element.elements[elementID] = [disp, trac]

if __name__ == "__main__":
    pass