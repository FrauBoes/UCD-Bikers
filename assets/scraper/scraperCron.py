
#!/usr/bin/python

import requests
#import urllib
import time
import json
import pymysql
import urllib.request,urllib.parse,json


url = "http://api.openweathermap.org/data/2.5/forecast?id=2964574&APPID=31f19a108384bc317e2d91c5621c791e";
with urllib.request.urlopen(url) as url:
    data = json.loads(url.read().decode('utf-8-sig'))
weather = data["list"][0]["weather"][0]["description"]
temperature = data["list"][0]["main"]["temp"]

host ="bikedata.c33719womxye.us-east-2.rds.amazonaws.com"
port = 3306
dbname="bikedata"
user = "aws137482dd"
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

    sql = """INSERT INTO BIKEDATA (STATION_NAME ,STATION_ADDRESS, STATION_NUMBER, STATUS, TIME, NUMBER_OF_STANDS,NUMBER_OF_BIKES, NUMBER_OF_SPACES, BANKING, TEMPERATURE, WEATHER) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    cursor.execute(sql,(station,statAddress,stationNum,status,Time,numStands,bikes,spaces,bank,temperature,weather))

    conn.commit()
    
conn.close()
