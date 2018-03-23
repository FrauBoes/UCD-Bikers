import urllib.request
import urllib.parse
import json

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
    
    for s in bikesInfo:
        number.append(s['number'])
        #name = s['name']
        #address = s['address']
        locations.append(s['position'])
        bikes_stands.append(s['bike_stands'])
        available_bikes.append(s['available_bikes'])
    return locations,number,bikes_stands,available_bikes

def topStation(stations):
    #  find the top station which has the most bikes.
    pass
    

if __name__=="__main__":
    print(initStations())