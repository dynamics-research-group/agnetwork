import unittest
from element import Element
from element import Beam
from element import Boundary
from unittest.mock import patch

class TestElementClass(unittest.TestCase):

    def setUp(self):
        # Create an instance of the Element class
        self.earth = Element('A')

    def tearDown(self):
        del self.earth

    def test_init(self):
        """Test the Element __init__ method"""
        # Check that instance of Element initialised correctly
        self.assertEqual(self.earth.elementID, 'A')
        self.assertEqual(Element.elements['A'], [])

    def test_remove(self):
        """Test the remove method"""
        # Test that remove method deletes dictionary entry for element
        self.earth.remove()
        with self.assertRaises(KeyError):
            Element.elements['A']
        # Check that trying to remove an entry that does not exist returns none
        self.assertIsNone(self.earth.remove())
    
    def test_removeConnections(self):
        """Test the removeConnections method"""
        Element.joints = {1: ['A','B'], 2: ['B','C']}
        self.earth.removeConnections()
        # Check that correct dictionary entry has been removed
        with self.assertRaises(KeyError):
            print(self.earth.joints[1])
        # Check that other joint still exists
        self.assertEqual(Element.joints[2], ['B','C'])
        del Element.joints

class TestBeamClass(unittest.TestCase):

    def setUp(self):
        # Create an instance of the Element class
        self.BeamA = Beam('A')

    def tearDown(self):
        del self.BeamA

    def test_init(self):
        """Test the Beam __init__ method"""
        # Check that instance of Beam initialised correctly
        self.assertEqual(self.BeamA.elementID, 'A')
        self.assertEqual(self.BeamA.length, 1)
        self.assertEqual(self.BeamA.mass, 1)
        self.assertEqual(Beam.elements['A'], [1, 1])

class TestBoundaryClass(unittest.TestCase):

    def setUp(self):
        # Create an instance of the Boundary class
        self.BC1 = Boundary(1)

    def tearDown(self):
        del self.BC1

    def test_init(self):
        """Test the Boundary __init__ method"""
        # Check that instance of Boundary initialised correctly
        self.assertEqual(self.BC1.elementID, 1)
        self.assertEqual(self.BC1.disp, 0)
        self.assertEqual(self.BC1.trac, 0)
        self.assertEqual(Boundary.elements[1], [0, 0])

if __name__ == '__main__':
    unittest.main()