import unittest
from element import Element
from unittest.mock import patch

class TestElementClass(unittest.TestCase):

    def setUp(self):
        # Create an instance of the Element class 
        self.a = Element('a')

    def tearDown(self):
        pass

    def test_init(self):
        # Check that instance of Element initialised correctly
        self.assertEqual(self.a.elementID, 'a')
        self.assertEqual(self.a.length, 1)
        self.assertEqual(self.a.mass, 1)

if __name__ == '__main__':
    unittest.main()