from structure import Structure

class Element(Structure):
    # Create an instance of elements with user-defined ID and default attributes
    def __init__(self,
                 elementID,
                 length=1,
                 mass=1):
        self.elementID = elementID
        self.length = length
        self.mass = mass