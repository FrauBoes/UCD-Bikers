# Script to fetch dynamic station data and create station list

import urllib.request
import urllib.parse
import json
import geopy
from geopy.distance import vincenty

# Set up stations on first load
def initStations():
    # Parse the URL and get bikes info
    url="https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=51f45929f155df8d4fdd5344aa62a33c9977b803"
    with urllib.request.urlopen(url) as req:
        bikesInfo = json.loads(req.read().decode("utf-8"))
    locations=[]
    number=[]
    bikes_stands =[]
    available_bikes =[]
    category=[]

    for s in bikesInfo:
        number.append(s['number'])
        locations.append(s['position'])
        bikes_stands.append(s['bike_stands'])
        available_bikes.append(s['available_bikes'])
        ava = s['available_bikes']/s['bike_stands']
        
        # Categorise stations based on number of bikes for icons
        if(s['status'] == 'CLOSED'):
            category.append(4)
        else:
            if(ava==0):
                category.append(0)
            elif(ava <=0.3):
                category.append(1)
            elif(ava > 0.3 and ava <= 0.6):
                category.append(2)
            else:
                category.append(3)
    return locations,number,bikes_stands,available_bikes,category


class station:
    """Class for each station"""
    
    def __init__(self, num, name, address, lat, lng, avabike, stands, status):
        self.number = num
        self.name =  name
        self.address = address
        self.lat = lat
        self.lng = lng
        self.availible_bike = avabike
        self.bike_stands = stands
        self.status = status
        self.initCategory()
        
        
    def initCategory(self):
        # Stations are grouped into five categories
        percent = self.availible_bike/self.bike_stands
        if(self.status == 'CLOSED'):
            self.category = 4
        else:
            if (percent == 0):
                self.category = 0
            elif(percent <= 0.3):
                self.category = 1
            elif(percent > 0.3 and percent <= 0.6):
                self.category = 2
            else:
                self.category = 3
                
                
    def getJSON(self):
        # Return the attribute as a json
        res = {"number": self.number,
               "name": self.name,
               "address": self.address,
               "lat": self.lat,
               "lng": self.lng, 
               "availible_bike": self.availible_bike,
               "bike_stands": self.bike_stands,
               "status": self.status,
               "category": self.category,
               "availible_space":int(self.bike_stands)-int(self.availible_bike)}
        return res
        

class  stationOperation:
    """Class to store all stations and define methods to handle station data"""
    
    # The default center of the map (By Dublin Castle)
    defaultCenter = (53.3439118,-6.2658777)
    
    # Distance between users' location and default center 
    defaultDistance = 2
    
    # Dynamatic API to get data
    url="https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=51f45929f155df8d4fdd5344aa62a33c9977b803"
    
    def __init__(self):
        self.stationDictionary = {}
        self.distanceDictionary = {}
        with urllib.request.urlopen(self.url) as req:
            JSONfile = json.loads(req.read().decode("utf-8"))
        self.loadJSON(JSONfile)
        self.updateMapCenter(self.defaultCenter)
        self.updateDistance(self.mapCenterCord)
    
    
    def loadJSON(self, JSONfile):
        # Read JSON file and conver to list
        for row in JSONfile:
            singleStation = station(row['number'],row['name'], row['address'],row['position']['lat'],row['position']['lng'],row['available_bikes'],row['bike_stands'],row['status'])
            self.stationDictionary.update({row['number']: singleStation})
    
    
    def countSingleDistance(self, cord1, cord2):
        # Calculate the distance between 2 tuples of coordinates(lat,lng):
        return geopy.distance.vincenty(cord1,cord2).km
            
        
    def updateDistance(self, cord):
        # Update station's distance from user location
        self.centerCord = cord;
        for key in self.stationDictionary.keys():
            stationCord = (self.stationDictionary[key].lat, self.stationDictionary[key].lng)
            self.distanceDictionary.update({key: self.countSingleDistance(self.centerCord, stationCord)})
            
            
    def getStationAndMapCenterJSON(self):
        # Return station info as JSON file
        stationJSON = {}
        for key in self.stationDictionary.keys():
            stationJSON.update({key: self.stationDictionary[key].getJSON()})
        stationJSON.update({"centerCord": {"lat": self.mapCenterCord[0], "lng":self.mapCenterCord[1]}})
        return stationJSON
    
    
    def getMapCenterJSON(self):
        # Return map centre as JSON
        return {"centerCord": {"lat": self.mapCenterCord[0], "lng": self.mapCenterCord[1]}}
    
    
    def updateMapCenter(self,cord):
        # Reset map location based on user coordinates
        self.mapCenterCord = cord
        if self.countSingleDistance(self.mapCenterCord, self.defaultCenter) > self.defaultDistance:
            self.mapCenterCord = self.defaultCenter
    
    
    def getListJSON(self):
        # Calculate distances from location to nearby stations
        # Return a JSON of nearest 3 stations
        sorted_key = []
        listJSON = []
        for key in sorted(self.distanceDictionary,key=self.distanceDictionary.get):
            sorted_key.append(key)
        number = 0
        for key in sorted_key:
            if self.stationDictionary[key].status == 'OPEN' and int(self.stationDictionary[key].availible_bike) != 0:
                listJSON.append(self.stationDictionary[key].getJSON())
                number=number +1 
            if number == 3:
                break
                
        return listJSON
    
    
    def updateList(self,cord):
        # On click update list
        self.updateDistance(cord)
        return self.getListJSON()
    
# Script test        
if __name__=="__main__":
    
    mapInstance = stationOperation()
    print(mapInstance.stationDictionary[34].bike_stands)
    print(mapInstance.getListJSON())
    print(mapInstance.getStationAndMapCenterJSON())
    mapInstance.updateMapCenter((52.2439118,-6.2658777))
    print(mapInstance.getListJSON())
    print(mapInstance.getStationAndMapCenterJSON())
