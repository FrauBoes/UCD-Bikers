import urllib.request
import urllib.parse
import json
from . import mapStation
from _ast import Num
from gettext import lngettext
#parse the url and get bikes info

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
        #name = s['name']
        #address = s['address']
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
        self.number = Num
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
    """Create a class with libray storing all stations and wrapping all the operations for the data"""
    
    def __init__(self, JSONfile):
        self.stationDictionary = {}
        self.distanceDictionary = {}
        self.loadJSON(JSONfile)
        
    
    def loadJSON(self, JSONfile):
        # load the json file which has been converted into list in python
        for row in JSONfile:
            singleStation = station(row['number'],row['name'], row['address'],row['position']['latitude'],row['position']['longitude'],row['available_bikes'],row['bike_stands'],row['status'])
            self.stationDictionary.update({row['number']: singleStation.getJSON})
            
            
if __name__=="__main__":
    print(initStations())