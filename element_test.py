import unittest
from element import Element

class TestElementClass(unittest.TestCase):

    def setUp(self):
        # Create an instance of the Element class 
        self.Ea = Element('a')

    def tearDown(self):
        pass

    def test_init(self):
        # Check that instance of Element initialised correctly
        self.assertEqual(self.Ea.elementID, 'a')
        self.assertEqual(self.Ea.length, 1)
        self.assertEqual(self.Ea.mass, 1)

if __name__ == '__main__':
    unittest.main()