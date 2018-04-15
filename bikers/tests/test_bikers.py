import os
import sys
from bikers.bikers import getOccupancy
sys.path.append('.')
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
        pass
    
    def test_bucket_occupancy(self):
        pass
        
    def test_convert_data(self):
        assert getOccupancy.convert_data(getOccupancy.get_station_occupancy(1, 1)) is sorted

if __name__ == "__main__":
    import sys;
    sys.argv = ['', 'Test.testName']
    unittest.main()
