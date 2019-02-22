from structure import Structure

class Joint(Structure):

    @staticmethod
    # If there are no elements, you cannot create a joint
    def checkForElements():
        try:
            check = Joint.elements
        except NameError:
            check = False
        if bool(check) == False:
            raise NameError("no elements to connect")
        else:
            return True

    def __init__(self,
                 jointID,
                 jointSet,
                 location):
        if self.checkForElements():
            self.jointID = jointID
            self.jointSet = jointSet
    
    @property
    def jointSet(self):
        return self.__jointSet
    
    @jointSet.setter
    def jointSet(self, jointSet):
        if len(jointSet) != 2:
            raise ValueError("jointSet must contain two elements")
        elif jointSet[0] in Joint.elements and jointSet[1] in Joint.elements:
            self.__jointSet = jointSet
        else:
            raise ValueError("jointSet must contain at least two existing elements.")
    
if __name__ == '__main__':
    pass