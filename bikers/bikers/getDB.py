import json
import pymysql
from builtins import str

# RDS cannot connect
host ="bikerz.cji0jregr8by.us-west-2.rds.amazonaws.com"
port = 3306
dbname="BikeData"
user = "bikerz"
password="bikerz123"

<<<<<<< HEAD
# host = "localhost"
# user = "root"
# password = "112358"
# dbname = "test_Dublinbikers"
=======
#host = "localhost"
#user = "root"
#assword = "112358"
#dbname = "test_Dublinbikers"
>>>>>>> map


    
def getDB(number):
    #lat = location["lat"]
    #lan = number
    conn = pymysql.connect(host=host, user=user, port=port, passwd=password,db=dbname)
    cursor = conn.cursor()
    
    print(number)
    
<<<<<<< HEAD
    sql = """SELECT available_bikes, store_time, status FROM BikeData WHERE number = {} ORDER BY store_time DESC LIMIT 3""".format(number)

=======
    sql = """SELECT NUMBER_OF_STANDS, NUMBER_OF_BIKES, STATUS, TIME FROM BIKEDATA WHERE STATION_NUMBER = {} ORDER BY TIME DESC LIMIT 10""".format(int(number))
    
    #sql = """SELECT available_bikes, store_time, status FROM realtimebikes WHERE number = {} ORDER BY store_time DESC LIMIT 3""".format(number)
    
>>>>>>> map
    cursor.execute(sql)
    
    data=cursor.fetchall()
    
    cursor.close()
    
    return str(data)

# returns a string with all occupancy numbers of a given station for the current weekday
def get_station_occupancy(number):
    conn = pymysql.connect(host, user=user, port=port, passwd=password,db=dbname)
    cursor = conn.cursor()
    
    sql = """SELECT NUMBER_OF_BIKES, NUMBER_OF_STANDS FROM BIKEDATA WHERE STATION_NUMBER = {} ORDER BY TIME DESC LIMIT 20""".format(number)

    cursor.execute(sql)
    
    data=cursor.fetchall()
    
    cursor.close()
    
    return str(data)
    
    
if __name__=="__main__":
    print(get_station_occupancy(37))