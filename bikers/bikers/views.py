# Script to run the app

import datetime
from flask import Flask, render_template, request, jsonify
from bikers import app
from . import getStationsAPI
from . import getWeatherAPI
from . import getOccupancy
from flask.json import jsonify
from . import getBikesGraph


# Initialize the map instance
mapInstance = getStationsAPI.stationOperation()


# Function to load on first request
@app.route('/')
def index():    
    # Get station data and weather
    locations,number,bike_stands,available_bikes,category= getStationsAPI.initStations()
    weather = getWeatherAPI.getWeather()
    
    mapInfo = mapInstance.getStationAndMapCenterJSON()

    # Get weekday and data
    weekday = datetime.datetime.today().weekday() + 2
    data = getOccupancy.convert_data(getOccupancy.get_station_occupancy(weekday, 8)) # default station 8 Saint Stephen's Green
    predictiondata = getBikesGraph.getModelData(8,mapInstance.stationDictionary[8].bike_stands)
    
    return render_template('index.html',locations=locations,number=number,bike_stands=bike_stands,available_bikes=available_bikes,weather=weather, weekday=weekday, data=data, category=category,predictiondata=predictiondata,mapInfo = mapInfo)


# Refresh graph on clicked station
@app.route('/getGraph')
def occupancy_graph():
    # Get station selected
    number = request.args.get('num')      
    
    # Get current weekday  
    weekday = datetime.datetime.today().weekday() + 2   
    
    # Get past occupancy data based on station and weekday    
    data = getOccupancy.convert_data(getOccupancy.get_station_occupancy(weekday, number))
    
    return jsonify(data)


# Center map on user location on first request
@app.route('/mapCenter')
def receive_location():
    latitude = request.args.get('lat')
    longitude = request.args.get('lng')
    mapInstance.updateMapCenter((latitude,longitude))
    return jsonify(mapInstance.getMapCenterJSON())


# Calculate list of nearest stations on given location
@app.route('/list')
def update_list():
    latitude = request.args.get('lat')
    longitude = request.args.get('lng')
    mapInstance.updateList((latitude,longitude))
    return jsonify(mapInstance.getListJSON())


@app.route('/getModel')
def bike_model():
    # Get station selected
    number = int(request.args.get('num'))
    
    # Get past occupancy data based on station and weekday    
    data = getBikesGraph.getModelData(number,mapInstance.stationDictionary[number].bike_stands)
    
    return jsonify(data)
    

