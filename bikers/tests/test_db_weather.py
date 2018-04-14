import sys
import pandas as pd
from pandas import DataFrame
import pymysql
import csv
import matplotlib.pyplot as plt



host ="bikedata.c33719womxye.us-east-2.rds.amazonaws.com"
port = 3306
dbname="BikeData"
user = "aws137482dd"
password="bikerz123"

conn = pymysql.connect(host, user=user, port=port, passwd=password,db=dbname)

cursor = conn.cursor()

sql = """SELECT TEMPERATURE, RAIN, TIME FROM WEATHERDATA """

cursor.execute(sql)

results = cursor.fetchall()

cfile = csv.writer(open("weather.csv","w"))

header = ('temperature', 'rain', 'time')

cfile.writerow(header)

for row in results:
        cfile.writerow(row)

conn.close()