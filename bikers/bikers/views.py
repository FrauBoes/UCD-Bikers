# Script to run all the vital components of the app

import datetime
from flask import Flask, render_template, request, jsonify
from bikers import app
from . import getStationsAPI
from . import getWeatherAPI
from . import getOccupancy
from flask.json import jsonify
from . import getModel


# Initialize the map instance
mapInstance = getStationsAPI.stationOperation()

@app.route('/')
def index():    
    # Get station data and weather
    locations,number,bike_stands,available_bikes,category= getStationsAPI.initStations()
    weather = getWeatherAPI.getWeather()
    
    mapInfo = mapInstance.getStationAndMapCenterJSON()

    # Get weekday and data
    weekday = datetime.datetime.today().weekday() + 2
    data = getOccupancy.convert_data(getOccupancy.get_station_occupancy(weekday, 8)) # default station 8 Saint Stephen's Green

    return render_template('index.html',locations=locations,number=number,bike_stands=bike_stands,available_bikes=available_bikes,weather=weather, weekday=weekday, data=data, category=category, mapInfo = mapInfo)

    
@app.route('/getGraph')
def occupancy_graph():
    # Get station selected
    number = request.args.get('num')      
    
    # Get current weekday  
    weekday = datetime.datetime.today().weekday() + 2   
    
    # Get past occupancy data based on station and weekday    
    data = getOccupancy.convert_data(getOccupancy.get_station_occupancy(weekday, number))
    
    return jsonify(data)

@app.route('/getstations')
def list_stations():
    #Get the longitude and latitude of searched place
    lat = float(request.args.get('lat'))
    lng = float(request.args.get('lng'))

    loc = (lat,lng)

    #Need to see if every station in the list has bikes

    M = mapStation.mapper()
    nearestStats = M.findClosest(loc)

    one = str(nearestStats[0])
    two = str(nearestStats[1])
    three = str(nearestStats[2])

    return jsonify(nearestStats)



@app.route('/mapCenter')
def receive_location():
    latitude = request.args.get('lat')
    longitude = request.args.get('lng')
    mapInstance.updateMapCenter((latitude,longitude))
    return jsonify(mapInstance.getMapCenterJSON())
    
@app.route('/list')
def update_list():
    latitude = request.args.get('lat')
    longitude = request.args.get('lng')
    mapInstance.updateList((latitude,longitude))
    return jsonify(mapInstance.getListJSON())
    
    
