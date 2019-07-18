from structure import Structure

class Joint(Structure):
    """Joints describing the geometric locations where elements meet each other"""
    @staticmethod
    def checkForElements():
        """Check whether or not any elements exist"""
        try:
            check = Joint.elements
        except NameError:
            check = False
        # check will be false if Joint.elements does not exist or if Joint.elements is empty
        if bool(check) == False:
            raise NameError("no elements to connect.")
        else:
            return True
    
    def __init__(self,
                 jointID,
                 jointSet,
                 location,
                 classification,
                 structureID='global'):
        if self.checkForElements():
            self.jointID = jointID
            self.structureID = structureID
            self.jointSet = jointSet
            self.location = location
            self.classification = classification
            if structureID not in Joint.joints:
                Joint.joints[structureID] = {}
            Joint.joints[structureID][jointID] = [jointSet, location, classification]
    
    @property
    def jointSet(self):
        return self.__jointSet
    
    @jointSet.setter
    def jointSet(self, jointSet):
        """Check that there are the correct number of elements in jointSet"""
        elements = Joint.elements[self.structureID].keys()
        if len(jointSet) != 2:
            raise ValueError("jointSet must contain two elements")
        # Check the existence of both elements in jointSet
        elif jointSet[0] and jointSet[0] in elements:
            self.__jointSet = jointSet
        else:
            raise ValueError("jointSet must contain two existing elements.")
    
class KinematicJoint(Joint):
    def __init__(self,
                 jointID,
                 jointSet,
                 location,
                 classification,
                 structureID='global',
                 disp_DoF=['x', 'y', 'z'],
                 rot_DoF=['x', 'y', 'z']):
        # Call standard joint initialisation
        Joint.__init__(self, jointID, jointSet, location, classification, structureID)
        self.disp_DoF = disp_DoF
        self.rot_DoF = rot_DoF
        Joint.joints[structureID][jointID].extend([disp_DoF, rot_DoF])

if __name__ == '__main__':
    pass