#!/usr/bin/python

import requests
import time
import json
import pymysql
import urllib.request,urllib.parse,json

host ="bikedata.c33719womxye.us-east-2.rds.amazonaws.com"
port = 3306
dbname="BikeData"
user = "aws137482dd"
password="bikerz123"

conn = pymysql.connect(host, user=user, port=port, passwd=password,db=dbname)

cursor = conn.cursor()

response = requests.get("http://api.openweathermap.org/data/2.5/weather?units=metric&id=2964574&APPID=31f19a108384bc317e2d91c5621c791e")

JO = response.json()

try:
        rain = JO["rain"]["3h"]
except KeyError:
        rain = 0
        
temperature = JO["main"]["temp"]
time = datetime.datetime.fromtimestamp(int(JO["dt"])).strftime('%d/%m/%Y %H:%M')

sql = """INSERT INTO WEATHERDATA (TEMPERATURE, RAIN, TIME) VALUES (%s,%s,%s)"""

cursor.execute(sql,(temperature,rain,time))

conn.commit()

conn.close()
