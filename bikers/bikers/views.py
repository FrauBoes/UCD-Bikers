import datetime
from flask import render_template, request
from bikers import app
from . import getStationsAPI
from . import getWeatherAPI
from . import getOccupancy

@app.route('/index')
def index():
    app.logger.warning('sample message')
    locations, number,bike_stands,available_bikes = getStationsAPI.initStations()
    weather = getWeatherAPI.weatherbroadcast()
    occupancy_graph(37)  # default station 37 can be changed to dynamic later on
    return render_template('index.html',locations=locations,number=number,bike_stands=bike_stands,available_bikes=available_bikes,weather=weather)

@app.route('/getdetail')
def get_station_no():
    number = request.args.get('num')
    occupancy_graph(number)
    # return occupancy_graph(number)

def occupancy_graph(number):
    weekday = datetime.datetime.today().weekday() + 1
    data = getOccupancy.get_station_occupancy(weekday, number)
    return render_template('occupancy.html', weekday=weekday, data=data)