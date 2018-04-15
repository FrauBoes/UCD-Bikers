import os
import sys
sys.path.append('.')
from bikers import bikers  
import unittest
import tempfile
from bikers import getStationsAPI


mapInstance = getStationsAPI.stationOperation()

print(mapInstance.getListJSON())

print(mapInstance.getStationAndMapCenterJSON())

