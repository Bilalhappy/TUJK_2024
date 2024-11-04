import os
import numpy as np
import pandas as pd
import datetime
import time
import psypy.psySI as SI
import matplotlib.pyplot as plt
from metpy.calc import wet_bulb_temperature
from metpy.calc import dewpoint_from_relative_humidity
from metpy.units import units

f = open("ISTA00XXX_R_20210010000_00U_01H_MM.rnx","r")
data = f.readlines()
f.close()
for i in range(len(data)):
    if data[i].split()[0] == "END":
        break
del data[:i+1]

press = []
T = []
rh = []
S = []
date = []
for i in range(len(data)):
    dd = str(data[i].split()[0]+data[i].split()[1]+data[i].split()[2]+data[i].split()[3])
    date.append(datetime.datetime.strptime(dd,"%Y%m%d%H"))
    press.append(float(data[i].split()[8]))
    T.append(float(data[i].split()[10]))
    rh.append(float(data[i].split()[7]))
    try:
        S.append(wet_bulb_temperature(press[-1] * units.hPa, T[-1] * units.degC, dewpoint_from_relative_humidity(T[-1] * units.degC,rh[-1]* units.percent)))
    except:
        S.append(S[-1])

df = pd.DataFrame(list(zip(date,press,T,rh,S)),columns=["date","press.","DryT","Hum.","WetT"])
print(df)

df["time"] = pd.to_datetime(df["date"])

df['time'] = df['time'].apply(lambda dt: datetime.datetime(dt.year, dt.month, dt.day, dt.hour,60*(dt.minute // 60)))
df['date'] = df['date'].apply(lambda dt: datetime.datetime(dt.year, dt.month, dt.day, dt.hour,60*(dt.minute // 60)))

min_date = df.time.min()
max_date = df.time.max()
dates_range = pd.date_range(min_date, max_date, freq = '30min')
df.set_index('date', inplace=True)
df3=pd.DataFrame(dates_range).set_index(0)
df4 = df3.join(df)
print(df4)
df = df4.fillna(method="bfill")
print(df)
df.to_excel("meteo_RNX.xlsx")
plt.plot(df.index,df["DryT"])
plt.show()
