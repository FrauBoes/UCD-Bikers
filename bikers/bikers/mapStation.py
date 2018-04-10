# This module works for calculateing the top station depending on the user geolocation and station.
import geopy
from geopy.distance import vincenty
import json


class mapper:
    """Creates a class with all of the station locations as tuples as a list"""
    # Will contain coordinates of all stations
    stationCoords = []

    # Creates a list of tuples of (station number, latitude, longitude)
    def __init__(self):
        with open('../../assets/stations.json') as data_file:
            data = json.loads(data_file.read())
        # Iterate through JSON file and create tuples and add to list
        for x in data:
            station = x['number']
            lat = x['latitude']
            long = x['longitude']
            self.stationCoords += [(station, lat, long)]

    # Finds the distance between 2 tuples of coordinates (lat,long)
    def findDistance(self, coord1, coord2):
        return geopy.distance.vincenty(coord1, coord2).km

    #Function that takes input of user location and compares to all station locations and returns the 3 closest

    def findClosest(self,location):
        # Initialise distances to arbitrarily high values so the first few values will be written
        first,second,third = 10000,10000,10000

        for x in self.stationCoords:
            StCoords = (x[1],x[2])
            dist = self.findDistance(location,StCoords)
            if dist < third:
                if dist < second:
                    if dist < first:
                        first = dist
                        station1 = x[0]
                    else:
                        second = dist
                        station2 = x[0]
                else:
                    third = dist
                    station3 = x[0]
        #Returns tuple with the 3 closest stations numbers
        return (station1,station2,station3)