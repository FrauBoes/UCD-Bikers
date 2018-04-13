# This module works for calculateing the top station depending on the user geolocation and station.
import geopy
from geopy.distance import vincenty
import json

from operator import itemgetter


class mapper:
    """Creates a class with all of the station locations as tuples in a list"""
    # Will contain coordinates of all stations
    stationCoords = []
    
    #with open(os.path.join(os.path.dirname(__file__),'stations.json'), 'r')as data_file:


    # Creates a list of tuples of (station number, latitude, longitude)
    def __init__(self):

        with open('/home/daragh/Project/UCD-Bikers/bikers/bikers/static/stations.json') as data_file:

            data = json.loads(data_file.read())
        # Iterate through JSON file and create tuples and add to list
        for x in data:
            station = x['number']
            lat = x['latitude']
            long = x['longitude']
            avail = x['available_bikes']
            self.stationCoords += [(station, lat, long, avail)]

    # Finds the distance between 2 tuples of coordinates (lat,long)
    def findDistance(self, coord1, coord2):
        return geopy.distance.vincenty(coord1, coord2).km

    # Function that takes input of user location and compares to all station locations and returns the 6 closest with station info

    def findClosest(self,location):
        # Initialise list of tuples in the form (distance,station number, bikes available) distances set to arbitrarily high values so the first few values will be written

        rank = [(10000,0,0)]*6
        for x in self.stationCoords:
            StCoords = (x[1],x[2])
            dist = self.findDistance(location,StCoords)


            # Compare distance to greatest distance in list. Replace if smaller.
            if dist< rank[5][0]:
                rank[5] = (dist, x[0], x[3])

            # Sort list so furthest away is at the end of the list (item getter specifies which item in the tuple to rank by
            rank = sorted(rank, key=itemgetter(0))

        return rank
