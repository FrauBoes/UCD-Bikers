import json
import pymysql

# RDS cannot connect
host ="bikerz.cji0jregr8by.us-west-2.rds.amazonaws.com"
port = 3306
dbname="BikeData"
user = "bikerz"
password="bikerz123"

#host = "localhost"
#user = "root"
#assword = "112358"
#dbname = "test_Dublinbikers"


    
def getDB(number):
    #lat = location["lat"]
    #lan = number
    conn = pymysql.connect(host=host, user=user, port=port, passwd=password,db=dbname)
    cursor = conn.cursor()
    
    print(number)
    
    sql = """SELECT NUMBER_OF_STANDS, NUMBER_OF_BIKES, STATUS, TIME FROM BIKEDATA WHERE STATION_NUMBER = {} ORDER BY TIME DESC LIMIT 10""".format(int(number))
    
    #sql = """SELECT available_bikes, store_time, status FROM realtimebikes WHERE number = {} ORDER BY store_time DESC LIMIT 3""".format(number)
    
    cursor.execute(sql)
    
    data=cursor.fetchall()
    
    cursor.close()
    
    return str(data)

    
if __name__=="__main__":
    print(getDB(3))