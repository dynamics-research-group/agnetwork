import unittest
from joint import Joint
from joint import KinematicJoint
from unittest.mock import patch

class TestJointClass(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        # Check that when a joint is created between two elements that exist
        with patch.object(Joint, "elements"):
            with self.assertRaisesRegex(ValueError, "jointSet must contain two elements"):
                Joint(1, [], [0, 0], 'Bolted')
            with self.assertRaisesRegex(ValueError, "jointSet must contain two existing elements"):
                Joint(1, ['A','B'], [0, 0], 'Bolted')
        # Check that joint initialises correctly when connecting two elements
        Joint.elements['global'] = {'A': [], 'B': [], 'C': []}
        j1 = Joint(1, ['A','B'], [0, 0], 'Bolted')
        self.assertEqual(j1.jointID, 1)
        self.assertEqual(j1.jointSet, ['A','B'])
        self.assertEqual(j1.location, [0, 0])
        self.assertEqual(j1.classification, 'Bolted')
        self.assertEqual(Joint.joints['global'][1], [['A','B'], [0, 0], 'Bolted'])
        j2 = Joint(2, ['B','C'], [0, 0], 'Bolted')
        self.assertEqual(j2.jointID, 2)
        self.assertEqual(j2.jointSet, ['B','C'])
        self.assertEqual(Joint.joints['global'][2], [['B','C'], [0, 0], 'Bolted'])

    def test_checkForElements(self):
        # Check that the correct error is raised if Joint.elements does not exist
        with self.assertRaisesRegex(NameError, "no elements to connect."):
            Joint.checkForElements()
        # Check that the correct error is raised if Joint.elements is empty
        with patch.object(Joint, "elements"):
            Joint.elements = {}
            with self.assertRaisesRegex(NameError, "no elements to connect."):
                Joint.checkForElements()
        # Check that no error is raised when Joint.elements contains at least one element      
        with patch.object(Joint, "elements"):
            Joint.elements = {'A'}
            self.assertEqual(Joint.checkForElements(), True)

class TestKinematicJointClass(unittest.TestCase):

    def test_init(self):
        # Check that joint initialises correctly when connecting two elements
        Joint.elements['global'] = {'A': [], 'B': []}
        kj1 = KinematicJoint(1, ['A','B'], [0, 0], 'Bearing')
        self.assertEqual(kj1.jointID, 1)
        self.assertEqual(kj1.jointSet, ['A','B'])
        self.assertEqual(kj1.location, [0, 0])
        self.assertEqual(kj1.classification, 'Bearing')
        self.assertEqual(kj1.disp_DoF, ['x', 'y', 'z'])
        self.assertEqual(kj1.rot_DoF, ['x', 'y', 'z'])
        self.assertEqual(Joint.joints['global'][1], [['A','B'], 
                                                     [0, 0], 
                                                     'Bearing', 
                                                     ['x', 'y', 'z'], 
                                                     ['x', 'y', 'z']])

if __name__ == '__main__':
    unittest.main()