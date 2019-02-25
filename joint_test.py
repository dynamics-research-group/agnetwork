import unittest
from joint import Joint
from unittest.mock import patch

class TestJointClass(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        # Check that when a joint is created between two elements that exist
        with patch.object(Joint, "elements", return_value = {'a'}):
            with self.assertRaisesRegex(ValueError, "jointSet must contain two elements"):
                Joint(1, [], [0,0])
            with self.assertRaisesRegex(ValueError, "jointSet must contain two existing elements"):
                Joint(1, ['a','b'], [0,0])
        # Check that joint initialises correctly when connecting two elements
        with patch.object(Joint, "elements"):
            Joint.elements = {'a','b'}
            J1 = Joint(1, ['a','b'], [0,0])
            self.assertEqual(J1.jointID, 1)
            self.assertEqual(J1.jointSet, ['a','b'])
            self.assertEqual(J1.location, [0,0])

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
            Joint.elements = {'a'}
            self.assertEqual(Joint.checkForElements(), True)

if __name__ == '__main__':
    unittest.main()