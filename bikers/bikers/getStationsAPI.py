import urllib.request
import urllib.parse
import json
from . import mapStation
#parse the url and get bikes info

def initStation():
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

def topStation(stations):
    #  find the top station which has the most bikes.
    pass


def initStationInstance():
        #parse the URL and get bikes info
    url="https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=51f45929f155df8d4fdd5344aa62a33c9977b803"
    with urllib.request.urlopen(url) as req:
        bikesInfo = json.loads(req.read().decode("utf-8"))
        
    # declare class instance list
    stations=[]
    
    
    

 
 
 
 

if __name__=="__main__":
    print(initStations())