import json
import pymysql
from builtins import list
from datetime import datetime
from collections import OrderedDict

host ="bikerz.cji0jregr8by.us-west-2.rds.amazonaws.com"
port = 3306
dbname="BikeData"
user = "bikerz"
password="bikerz123"
    
    
# returns a tuple of tuples with all rows of occupancy and timestamp for a given station and weekday (1=Sunday, 7=Saturday)
def get_station_occupancy(weekday,number):
    conn = pymysql.connect(host, user=user, port=port, passwd=password,db=dbname)
    cursor = conn.cursor()
    sql = """SELECT TIME, NUMBER_OF_BIKES, NUMBER_OF_STANDS FROM BIKEDATA WHERE DAYOFWEEK(FROM_UNIXTIME(TIME/1000)) = {} AND STATION_NUMBER = {} ORDER BY TIME ASC""".format(weekday,number)
    cursor.execute(sql)
    data=cursor.fetchall()
    cursor.close()
    #print(data)
    return tuple(data)


# returns occupancy data as array of arrays [time, degree of availability]
def convert_data(data):
    occupancy_array = [['Time of the day', 'Degree of availability']]
    d = {}  # dictionary to store and aggregate entries based on time bin
    
    for entry in data:
        hour, minute = get_hour(entry[0]), get_minute(entry[0])
        time = round(hour + minute*0.1,1)  # time in format hh.m (6 bins)
        avail = entry[1]/entry[2]  # number of bikes / number of stands
        
        # get average of availability per time bin
        if time in d:
            d[time] = (d[time] + avail) / 2
        else:
            d[time] = avail
    
    # sort entries in dictionary to get chronologically sorted time bins
    d = OrderedDict(sorted(d.items()))
    
    for pair in d:
        inner_array = []
        inner_array.append(pair)
        inner_array.append(round(d[pair],2))
        occupancy_array.append(inner_array)
    
    return occupancy_array


# returns a tuple with hour (0-23) and minute frame (0-5)
def get_hour(timesstamp):
    hour = int(datetime.fromtimestamp(timesstamp / 1000).strftime('%H'))
    return hour


# returns a tuple with hour (0-23) and minute frame (0-5)
def get_minute(timesstamp):
    minute = round((int(datetime.fromtimestamp(timesstamp / 1000).strftime('%M')) // 10),1)
    return minute

 
# if __name__=="__main__":
#     print(convert_data(get_station_occupancy(4, 10)))