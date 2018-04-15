import urllib.request
import urllib.parse
import json
import geopy
from geopy.distance import vincenty



def initStations():
    #parse the URL and get bikes info
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
    """create a station to store all the station object"""
    
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
        # All stations are grouped into five categories
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
        # return the attribute as a json
        res = {"number": self.number,
               "name": self.name,
               "address": self.address,
               "lat": self.lat,
               "lng": self.lng, 
               "availible_bike": self.availible_bike,
               "bike_stands": self.bike_stands,
               "status": self.status,
               "category": self.category}
        return res
        

class  stationOperation:
    """Create a class with library storing all stations and wrapping all the operations for the data
    
    package all the variables and methods in the same class"""
    
    # the default center of the map
    defaultCenter = (53.3439118,-6.2658777)
    
    # Distance between users' location and our default center 
    defaultDistance = 2
    
    # The dynamatic API to get data
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
        # load the json file which has been converted into list in python
        for row in JSONfile:
            singleStation = station(row['number'],row['name'], row['address'],row['position']['lat'],row['position']['lng'],row['available_bikes'],row['bike_stands'],row['status'])
            self.stationDictionary.update({row['number']: singleStation})
    
    def countSingleDistance(self, cord1, cord2):
        # Count the distance between 2 tuples of coordinates(lat,lng):
        return geopy.distance.vincenty(cord1,cord2).km
            
    def updateDistance(self, cord):
        # update all the station's distance with user location
        self.centerCord = cord;
        for key in self.stationDictionary.keys():
            stationCord = (self.stationDictionary[key].lat, self.stationDictionary[key].lng)
            self.distanceDictionary.update({key: self.countSingleDistance(self.centerCord, stationCord)})
            
    def getStationAndMapCenterJSON(self):
        #return all the station info as JSON file.
        stationJSON = {}
        for key in self.stationDictionary.keys():
            stationJSON.update({key: self.stationDictionary[key].getJSON()})
        stationJSON.update({"centerCord": {"lat": self.mapCenterCord[0], "lng":self.mapCenterCord[1]}})
        return stationJSON
    
    def getMapCenterJSON(self):
        # After getting users' cord , it i s better to rest the map' location
        return {"centerCord": {"lat": self.mapCenterCord[0], "lng": self.mapCenterCord[1]}}
        
    
    def updateMapCenter(self,cord):
        # Compare with user's location
        # Map center only change once
        self.mapCenterCord = cord
        if self.countSingleDistance(self.mapCenterCord, self.defaultCenter) > self.defaultDistance:
            self.mapCenterCord = self.defaultCenter
    
    def getListJSON(self):
        # return sorted distance dict as a JSON file
        # sort distance dictionary
        sorted_key = []
        listJSON = []
        for key in sorted(self.distanceDictionary,key=self.distanceDictionary.get):
            sorted_key.append(key)
        for key in sorted_key[0:3]:
            listJSON.append(self.stationDictionary[key].getJSON()) 
                   
        return listJSON
    
    def updateList(self,cord):
        #Click and return all the list information
        self.updateDistance(cord)
        return self.getListJSON()


        
if __name__=="__main__":
    
    mapInstance = stationOperation(bikesInfo)
    print(mapInstance.getListJSON())
    print(mapInstance.getStationAndMapCenterJSON())
    mapInstance.updateMapCenter((52.2439118,-6.2658777))
    print(mapInstance.getListJSON())
    print(mapInstance.getStationAndMapCenterJSON())