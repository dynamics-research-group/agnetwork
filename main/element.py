from structure import Structure
from structure import Network

class Element(Structure):
    """Create an instance of elements with user-defined ID"""
    def __init__(self,
                 elementID,
                 structureID):
        self.elementID = elementID
        self.structureID = structureID
        if structureID not in Element.elements:
            Element.elements[structureID] = {}
        Element.elements[structureID][elementID] = []
    
    def remove(self):
        """Removes the dictionary entry for the elements"""
        try:
            del Element.elements[structureID][self.elementID]
        except:
            return None
    
    def removeConnections(self):
        """Removes any joints connected to the element"""
        # Delete joints if they exist
        try:
            joints = list(Element.joints[self.structureID].keys())
            for jointID in joints:
                localJoint = Element.joints[self.structureID][jointID][0]
                if self.elementID in localJoint:
                    del Element.joints[self.structureID][jointID]
        # Return none if there are no joints associated
        except:
            return None
    
    def __del__(self):
        self.removeConnections()
        self.remove()

class IrreducibleElement(Element):
    """Create a beam element with default attributes"""
    def __init__(self,
                 elementID,
                 structureID='global',
                 material=None,
                 geometry=1):
        Element.__init__(self, elementID, structureID)
        self.material = material
        self.geometry = geometry
        Element.elements[structureID][elementID] = [material, geometry]

class Boundary(Element):
    """Create a boundary condition with default attributes"""
    def __init__(self,
                 elementID,
                 structureID='global',
                 boundary = 'Ground'):
        Element.__init__(self, elementID, structureID)
        self.boundary = boundary
        Element.elements[structureID][elementID] = [boundary]

if __name__ == "__main__":
    pass