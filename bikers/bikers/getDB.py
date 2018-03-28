import json
import pymysql
from builtins import str

host ="bikerz.cji0jregr8by.us-west-2.rds.amazonaws.com"
port = 3306
dbname="BikeData"
user = "bikerz"
password="bikerz123"

    
# returns a string with all occupancy numbers of a given station for the current weekday
def get_station_occupancy(number):
    conn = pymysql.connect(host, user=user, port=port, passwd=password,db=dbname)
    cursor = conn.cursor()
    
    sql = """SELECT NUMBER_OF_BIKES, NUMBER_OF_STANDS FROM BIKEDATA WHERE STATION_NUMBER = {} ORDER BY TIME DESC LIMIT 20""".format(number)

    cursor.execute(sql)
    
    data=cursor.fetchall()
    
    cursor.close()
    
    return str(data)
    
   
# if __name__=="__main__":
#     print(get_station_occupancy(37))