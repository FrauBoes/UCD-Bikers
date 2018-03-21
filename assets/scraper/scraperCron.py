#!/usr/bin/python

import requests
import urllib
import time
import json
import pymysql

host ="bikerz.cji0jregr8by.us-west-2.rds.amazonaws.com"
port = 3306
dbname="BikeData"
user = "bikerz"
password="bikerz123"

conn = pymysql.connect(host, user=user, port=port, passwd=password,db=dbname)

cursor = conn.cursor()


api_key = '5a236d2bcaa8f6a83e1687d8243f4897ec78a8d8'

response = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=5a236d2bcaa8f6a83e1687d8243f4897ec78a8d8")

JO = response.json()

for i in range(len(JO)):
       	station = JO[i]['name']
        statAddress = JO[i]['address']
        stationNum = JO[i]['number']
	status = JO[i]['status']
        numStands = JO[i]['bike_stands']
        spaces = JO[i]['available_bike_stands']
        bikes = JO[i]['available_bikes']
        Time = JO[i]['last_update']
        bank = JO[i]['banking']

	sql = """INSERT INTO BIKEDATA (
                         STATION_NAME ,STATION_ADDRESS, STATION_NUMBER, STATUS, TIME, NUMBER_OF_STANDS,NUMBER_OF_BIKES, NUMBER_OF_SPACES, BANKING)
                         VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        cursor.execute(sql,(station,statAddress,stationNum,status,Time,numStands,bikes,spaces,bank))

        conn.commit()
	
	
conn.close()


