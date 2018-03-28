import json
import pymysql
from builtins import list
from datetime import datetime

host ="bikerz.cji0jregr8by.us-west-2.rds.amazonaws.com"
port = 3306
dbname="BikeData"
user = "bikerz"
password="bikerz123"
    
# returns a tuple of tuples with all rows of occupancy and timestamp for a given station and weekday (1=Sunday, 7=Saturday)
def get_station_occupancy(weekday,number):
    conn = pymysql.connect(host, user=user, port=port, passwd=password,db=dbname)
    
    cursor = conn.cursor()
    
    sql = """SELECT TIME, NUMBER_OF_BIKES, NUMBER_OF_STANDS FROM BIKEDATA WHERE DAYOFWEEK(FROM_UNIXTIME(TIME/1000)) = {} AND STATION_NUMBER = {} ORDER BY TIME ASC LIMIT 100""".format(weekday,number)
    
    cursor.execute(sql)
    
    data=cursor.fetchall()
    
    cursor.close()
    
    return tuple(data)

# returns a tuple with hour (0-23) and minute frame (0-5)
def get_timeframe(timesstamp):
    hour = int(datetime.fromtimestamp(timesstamp / 1000).strftime('%H'))
    
    minute = int(datetime.fromtimestamp(timesstamp / 1000).strftime('%M')) // 10  
       
    return hour, minute


if __name__=="__main__":
    print(get_timeframe(1522274403000))