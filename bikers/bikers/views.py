import datetime
from flask import render_template, request
from bikers import app
from . import getStationsAPI
from . import getWeatherAPI
from . import getOccupancy

@app.route('/')
def index():
    app.logger.warning('sample message')
    locations, number,bike_stands,available_bikes,category= getStationsAPI.initStations()
    weather = getWeatherAPI.weatherbroadcast()
    
    # weekday and data for occupancy.html
    weekday = datetime.datetime.today().weekday() + 2
    data = getOccupancy.convert_data(getOccupancy.get_station_occupancy(weekday, 37)) # default station, to be changed later
    
    return render_template('index.html',locations=locations,number=number,bike_stands=bike_stands,available_bikes=available_bikes,weather=weather, weekday=weekday, data=data, category=category)


@app.route('/getdetail')
def occupancy_graph():
    number = request.args.get('num')
    weekday = datetime.datetime.today().weekday() + 2
    data = getOccupancy.convert_data(getOccupancy.get_station_occupancy(weekday, number))
    return render_template('occupancy.html', weekday=weekday, data=data)

