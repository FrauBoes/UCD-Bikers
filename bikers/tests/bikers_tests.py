import os
from bikers import bikers  
import unittest
import tempfile

class BikersTestCase(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass

    def test_occupancy(self):
        assert bikers.views.occupancy_graph(37) is not None;

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()