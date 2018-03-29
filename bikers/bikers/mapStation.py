#This module works for calculateing the top station depend on the user geolocation and station.
 
 import geopy.geocoders import vincenty
 

     

class mapStation:
    
    """A class representing a Station"""
    
    
     def __init__(self, lat, lon, center, number,avabikes,stands,status):
         self.latitude = lat
         self.longitude = lon
         self.number = number
         self.available_bikes=avabikes
         self.bike_stands = stands
         self.status = status
         countDistance(center)
         setCategory()
         
    def countDistance(self, center = (53.3439118,-6.2658777)):
        station_cord = (self.latitude, self.longitude)
        self.distance = vincenty(station_cord, center).miles
        
    def setCategory(self):
        ava = self.available_bikes / self.bike_stands
        if(self.status = "CLOSED"):
            self.category = 4
        else:
            if(ava==0):
                self.category = 0
            elif(ava <=0.3):
                self.category = 1
            elif(ava > 0.3 and ava <= 0.6):
                self.category = 2
            else:
                self.category = 3
        