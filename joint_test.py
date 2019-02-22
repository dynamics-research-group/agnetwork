import unittest
from joint import Joint
from unittest.mock import patch

class TestJointClass(unittest.TestCase):

    def setUp(self):
        # Create an instance of the Element class 
        self.J1 = Joint(1,['a','b'],[0,0])

    def tearDown(self):
        pass

    def test_init(self):
        pass

if __name__ == '__main__':
    unittest.main()