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
                 location):
        if self.checkForElements():
            self.jointID = jointID
            self.jointSet = jointSet
            self.location = location
            Joint.joints[jointID] = [jointSet, location]
    
    @property
    def jointSet(self):
        return self.__jointSet
    
    @jointSet.setter
    def jointSet(self, jointSet):
        """Check that there are the correct number of elements in jointSet"""
        if len(jointSet) != 2:
            raise ValueError("jointSet must contain two elements")
        # Check the existence of both elements in jointSet
        elif jointSet[0] in Joint.elements and jointSet[1] in Joint.elements:
            self.__jointSet = jointSet
        else:
            raise ValueError("jointSet must contain two existing elements.")
    
if __name__ == '__main__':
    pass