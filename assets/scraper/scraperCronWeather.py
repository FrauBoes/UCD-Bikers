<<<<<<< HEAD
=======

>>>>>>> 50d995bc950e6e2551bb27f090b249fb3513ff52
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

response = requests.get("http://api.openweathermap.org/data/2.5/forecast?id=2964574&APPID=31f19a108384bc317e2d91c5621c791e")

JO = response.json()

weather = JO["list"][0]["weather"][0]["description"]
temperature = JO["list"][0]["main"]["temp"]
time = JO["list"][0]["dt_txt"]

sql = """INSERT INTO WEATHERDATA (TEMPERATURE, WEATHER, TIME) VALUES(%s,%s,%s)"""

cursor.execute(sql,(temperature,weather, time))

conn.commit()
    
conn.close()
