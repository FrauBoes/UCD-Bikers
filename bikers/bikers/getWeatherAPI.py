# Script to fetch weather data from API 

import urllib.request,urllib.parse,json

def getWeather():
    url = "http://api.openweathermap.org/data/2.5/forecast?id=2964574&APPID=31f19a108384bc317e2d91c5621c791e";
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode('utf-8-sig'))
    # Return only the data for the next 24 hours
    return data["list"][0:9]

