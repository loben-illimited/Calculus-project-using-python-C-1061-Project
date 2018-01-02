
# 經過網路取得資料
這篇文中的API key為我所申請


## 透過Google Maps Geocoding API 取得地點經緯度
好處是使用者能輸入**“任何語言”**也可取得該地點的準確經緯度

遇到的困難：
1. 當使用者輸入中文時 `url` urlopen 將會出現error message，原因是未將ascii code外的文字作URL encoding


```python
# -*- coding: utf-8 -*-
import json #我們將會處理json資料
from urllib.request import urlopen #use urllib to open website
from urllib.parse import quote #處理使用者輸入英文外地址的問題

api_key = "AIzaSyBWr7l1Mv_2aFrjx2OTwVBmS78L5Dtfruo" #Geocoding API key
location = quote(input("地點： ")) #使用quote將文字作URL encoding
language = "zh-TW" #可用語言請參考 https://developers.google.com/maps/faq?authuser=1&hl=zh-tw#languagesupport

url = "https://maps.googleapis.com/maps/api/geocode/json?key="+api_key+"&address="+location+"&language="+language
json_data = urlopen(url).read().decode("utf8") #將取得的data順帶編碼

#print(json_data) #pring json

jsonObj = json.loads(json_data) #create json object

address = jsonObj.get("results")[0].get("formatted_address")
lat = jsonObj.get("results")[0].get("geometry").get("location").get("lat")
lng = jsonObj.get("results")[0].get("geometry").get("location").get("lng")
print("地點全稱：", address)
print("lat:", lat)
print("lng:", lng)
```

    地點： Beijing
    地點全稱： 中國北京市北京
    lat: 39.90419989999999
    lng: 116.4073963
    

## 利用Sunset and sunrise times API取得日出日落時間
我們將透過[Sunset and sunrise times API](https://sunrise-sunset.org/api)的API去取得地球上任何一個角落的日出日落時間

> Parameters(其參數)
* lat (float): Latitude in decimal degrees. Required.
* lng (float): Longitude in decimal degrees. Required.
* date (string): Date in YYYY-MM-DD format. Also accepts other date formats and even relative date formats. If not present, date defaults to current date. Optional.
* callback (string): Callback function name for JSONP response. Optional.
* formatted (integer): 0 or 1 (1 is default). Time values in response will be expressed following ISO 8601 and day_length will be expressed in seconds. Optional.




```python
# -*- coding: utf-8 -*-
import json #我們將會處理json資料
from urllib.request import urlopen #use urllib to open website

date = "today" #date format: YYYY-MM-DD
#以中央大學的地址作為測試取得日出日落時間的例子
lat = str(24.9694808)
lng = str(121.1925163)
formatted = str(0) #不進行格式處理，以方便後續處理

url = "https://api.sunrise-sunset.org/json?lat="+lat+"&lng="+lng+"&date="+date+"&formatted="+formatted
json_data = urlopen(url).read().decode("utf8")

#print(json_data) #print json data

jsonObj = json.loads(json_data)

sunrise_time_str = jsonObj.get("results").get("sunrise")
sunset_time_str = jsonObj.get("results").get("sunset")
print("日出時間(UTC):", sunrise_time_str)
print("日落時間(UTC):", sunset_time_str)

import datetime #處理時間用
sunrise_time = datetime.datetime.strptime(sunrise_time_str, "%Y-%m-%dT%H:%M:%S+00:00")
sunset_time = datetime.datetime.strptime(sunset_time_str, "%Y-%m-%dT%H:%M:%S+00:00")
print("sunrise_time : ", sunrise_time)
print("sunset_time : ", sunset_time)
```

    日出時間(UTC): 2017-12-23T22:37:17+00:00
    日落時間(UTC): 2017-12-24T09:12:39+00:00
    sunrise_time :  2017-12-23 22:37:17
    sunset_time :  2017-12-24 09:12:39
    

## timezone offset
因為datetime貌似不能保存時間的時區
故又使用google timezone api取得該經緯度的時間
為了方便程式設計，讓使用者直接輸入經緯度也能取得該地點的時區

並且參考了[Convert datetime to unix timestamp](http://quickies.seriot.ch/?id=397)將datetime object 轉換成unix time 以作為API的`timestamp`的參數

本人並不打算處理日光節約時間，所以`timestamp`的時間其實並非重點
並可以用`time`內的`time.time()`取得當前的unix time

而timezone offset則參考了[python time offset - Stack Overflow](https://stackoverflow.com/questions/14043934/python-time-offset?answertab=votes#tab-top)

* 而Google Timezone API請見[開發人員指南  |  Google Maps Time Zone API  |  Google Developers](https://developers.google.com/maps/documentation/timezone/intro?hl=zh-tw)


```python
# -*- coding: utf-8 -*-
import json #我們將會處理json資料
from urllib.request import urlopen #use urllib to open website

#以中央大學的地址作為例子
lat = str(24.9694808)
lng = str(121.1925163)
language = "zh-TW"
key = "AIzaSyBWr7l1Mv_2aFrjx2OTwVBmS78L5Dtfruo" #timezone API


import datetime
import time

sunrise_time = datetime.datetime(2017, 12, 23, 22, 37, 17)
sunrise_unix_time = time.mktime(sunrise_time.timetuple())
sunrise_unix_time = str(sunrise_unix_time)

url = "https://maps.googleapis.com/maps/api/timezone/json?location="+lat+","+lng+"&timestamp="+sunrise_unix_time+"&key="+key+"&language="+language
json_data = urlopen(url).read().decode("utf8")
#print("json data: \n", json_data)

jsonObj = json.loads(json_data)
rawOffset = jsonObj.get("rawOffset") #與UTC時間相差秒數
timeZoneID = jsonObj.get("timeZoneId")
timeZoneName = jsonObj.get("timeZoneName")
print("rawOffset", rawOffset, sep=": ")
print("timeZoneID", timeZoneID, sep=": ")
print("timeZoneName", timeZoneName, sep=": ")

print("\nUTC time: ", sunrise_time)
local_time = sunrise_time + datetime.timedelta(seconds = int(rawOffset)) #使用 "+" 是因為取得的rawOffset會帶正負號
print("local time: ", local_time)
```

    rawOffset: 28800
    timeZoneID: Asia/Taipei
    timeZoneName: 台北標準時間
    
    UTC time:  2017-12-23 22:37:17
    local time:  2017-12-24 06:37:17
    
