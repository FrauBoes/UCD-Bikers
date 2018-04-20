# Script to fetch the data for the occupancy chart
# Based on weekday and selected station

import json
import pymysql
from flask import jsonify
from builtins import list
from datetime import datetime
from collections import OrderedDict

# API access details
host ="bikedata.c33719womxye.us-east-2.rds.amazonaws.com"
port = 3306
dbname="BikeData"
user = "aws137482dd"
password="bikerz123"

    
# Returns a tuple of tuples with all rows of occupancy and timestamp for a given station and weekday (1=Sunday, 7=Saturday)
def get_station_occupancy(weekday,number):
    conn = pymysql.connect(host, user=user, port=port, passwd=password,db=dbname)
    cursor = conn.cursor()
    sql = """SELECT TIME, NUMBER_OF_BIKES, NUMBER_OF_STANDS FROM BIKEDATA WHERE DAYOFWEEK(FROM_UNIXTIME(TIME/1000)) = {} AND STATION_NUMBER = {} ORDER BY TIME ASC""".format(weekday,number)
    cursor.execute(sql)
    data=cursor.fetchall()
    cursor.close()
    return data


# Returns occupancy data as array of arrays [time, degree of availability]
def convert_data(data):
    occupancy_array = [['Time of the day', 'Degree of availability']]

    d = {}  # Dictionary to store and aggregate entries based on time bin
    
    for entry in data:

        hour, minute = get_hour(entry[0]), get_minute(entry[0])
        time = hour + (minute*0.5)+0.25  # time in format hh.m (1/2 hour bins)

        avail = int((entry[1]/entry[2])*100)  # Number of bikes / number of stands

        # Get average of availability per time bin for multiple entries
        if time in d:
            d[time] = (d[time] + avail) / 2
        else:
            d[time] = avail

    # Sort entries in dictionary to get chronologically sorted time bins
    d = OrderedDict(sorted(d.items()))
    
    for pair in d:
        inner_array = []
        inner_array.append(pair)
        inner_array.append(round(d[pair], 2))
        occupancy_array.append(inner_array)
    
    return occupancy_array


# Returns the hour
def get_hour(timesstamp):
    hour = int(datetime.fromtimestamp(timesstamp / 1000).strftime('%H'))
    return hour


# Returns the minutes rounded to half hour (it takes the decimal value when multiplied by 0.5 above)
def get_minute(timesstamp):
    minute = round(int(datetime.fromtimestamp(timesstamp / 1000).strftime('%M')) / 60, 0)
    return minute
