import datetime
from flask import Flask, render_template, request, jsonify
from bikers import app
from . import getStationsAPI
from . import getWeatherAPI
from . import getOccupancy

@app.route('/')
def index():
    app.logger.warning('sample message')
    
    # Get station data and weather
    locations,number,bike_stands,available_bikes,category= getStationsAPI.initStations()
    weather = getWeatherAPI.getWeather()
    
    # Get weekday and data
    weekday = datetime.datetime.today().weekday() + 2
    data = getOccupancy.convert_data(getOccupancy.get_station_occupancy(weekday, 8)) # default station 8 Saint Stephen's Green

    return render_template('index.html',locations=locations,number=number,bike_stands=bike_stands,available_bikes=available_bikes,weather=weather, weekday=weekday, data=data, category=category)

    
@app.route('/getdetail')
def occupancy_graph():
    # Get station selected
    number = request.args.get('num')      
    
    # Get current weekday  
    weekday = datetime.datetime.today().weekday() + 2   
    
    # Get past occupancy data based on station and weekday    
    data = getOccupancy.convert_data(getOccupancy.get_station_occupancy(weekday, number))
    
    return jsonify(data)


