from flask import render_template, request

from bikers import app


from . import getStationsAPI

from . import getWeatherAPI

from . import getDB

@app.route('/')
def index():
    app.logger.warning('sample message')
    locations, number,bike_stands,available_bikes =getStationsAPI.initStations()
    weather = getWeatherAPI.weatherbroadcast();
    return render_template('index.html',locations=locations,number=number,bike_stands=bike_stands,available_bikes=available_bikes,weather=weather)

@app.route('/getdetail')
def query():
    number = request.args.get('num')
    occupancy_graph(number)
    #print(getDB.getDB(number))
    return occupancy_graph(number)

def occupancy_graph(number):
    return render_template('occupancy.html', number=number)
