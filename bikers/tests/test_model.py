import urllib.request,urllib.parse,json
import statsmodels.api as smapi
import datetime
import sys
import pandas as pd
import numpy as np
from pandas import DataFrame
import statsmodels.api as smapi
import os

Maximum = 30
# get right now time
def getModelData(num, Maximum):
    now = datetime.datetime.now()

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    
    print(now.weekday())
    print(now.hour)
    print(THIS_FOLDER)
    
    url = "http://api.openweathermap.org/data/2.5/forecast?id=2964574&APPID=31f19a108384bc317e2d91c5621c791e";
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode('utf-8-sig'))
        
    initTimestamp =data["list"][0]["dt"]
    
    now = datetime.datetime.fromtimestamp(initTimestamp)
    weekday = now.weekday()
    hour = now.hour
    inittime = int(hour + weekday *24)
    
    columns =["STATION_NUMBER","weather_rain", "weather_temperature"]
    df_prediction = pd.DataFrame(columns = columns)
    
    df_prediction["STATION_NUMBER"] = df_prediction["STATION_NUMBER"].astype('category')
    df_prediction["weather_rain"] = df_prediction["weather_rain"].astype('float')
    df_prediction["weather_temperature"] = df_prediction["weather_temperature"].astype('float')
    
    for i in range(8):
        temp = data["list"][i]["main"]["temp"]-273.15
        try:
            rain = data["list"][i]["rain"]["3h"]
        except KeyError:
            rain = 0
        for j in range(3):
            df_prediction = df_prediction.append({"weather_rain": rain,
                    "weather_temperature": temp,
                    "STATION_NUMBER": num,
                   },ignore_index=True)
    res= []
    for i in range(24):
            model_name = THIS_FOLDER + '/pre_model/'+str(i+inittime)
            
            newlm=smapi.load(model_name)
            stamp = datetime.datetime.fromtimestamp(initTimestamp + 60 * 60 * i)
            time = stamp.strftime("%H: %M")
            pre =[time] 
            
            pre_percentage = int(newlm.predict(df_prediction.take([i])));
            if pre_percentage >= Maximum:
                pre_percentage = Maximum/Maximum
            else:
                pre_percentage=pre_percentage/Maximum
            
            pre.append(pre_percentage)
            
            res.append(pre)
            
            

    return res


print(getModelData(1, Maximum))
