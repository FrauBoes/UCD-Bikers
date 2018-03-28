import pytest

from bikers import bikers

from bikers import getStationsAPI

class BikersTestCase(object):

    def setUp(self):
        getStationsAPI.initStations()
        pass

    def test_index(self):
        pass
