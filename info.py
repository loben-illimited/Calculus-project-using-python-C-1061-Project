# -*- coding: utf-8 -*-
import json #我們將會處理json資料
from urllib.request import urlopen #use urllib to open website
from urllib.parse import quote #處理使用者輸入英文外地址的問題

#處理time offset問題
import datetime
import time

class Get_info:
    
    def __init__(self, location, api_key_for_geocoding, language, api_key_for_timezone):
        '''
        location 為地點
        api_key 為google api key
        language 為語言
        '''
        self.location = quote(location)
        self.api_key_for_geocoding = api_key_for_geocoding
        self.language = language
        self.api_key_for_timezone = api_key_for_timezone
        
    def get_lat_lng(self):
        url = "https://maps.googleapis.com/maps/api/geocode/json?key="+self.api_key_for_geocoding+"&address="+self.location+"&language="+self.language
        json_data = urlopen(url).read().decode("utf8") #將取得的data順帶編碼
        jsonObj = json.loads(json_data) #create json object
        try:
            self.address = jsonObj.get("results")[0].get("formatted_address")
            self.lat = jsonObj.get("results")[0].get("geometry").get("location").get("lat")
            self.lng = jsonObj.get("results")[0].get("geometry").get("location").get("lng")
            #Debug
            #print("地點全稱：", address)
            #print("lat:", self.lat)
            #print("lng:", self.lng)
        except:
            print("系統無法判斷你輸入的位置 ")
        return [self.lat, self.lng]
    
    def time_off_set(self):
        now = datetime.datetime.now()
        unix_time = time.mktime(datetime.datetime(now.year, now.month, now.day).timetuple())
        url = "https://maps.googleapis.com/maps/api/timezone/json?location="+str(self.lat)+","+str(self.lng)+"&timestamp="+str(unix_time)+"&key="+self.api_key_for_timezone+"&language="+self.language
        json_data = urlopen(url).read().decode("utf8")
        #print("json data: \n", json_data)
        try:
            jsonObj = json.loads(json_data)
            self.rawOffset = jsonObj.get("rawOffset") #與UTC時間相差秒數
            self.timeZoneID = jsonObj.get("timeZoneId")
            self.timeZoneName = jsonObj.get("timeZoneName")
            #Debug
            #print("rawOffset", self.rawOffset, sep=": ")
            #print("timeZoneID", self.timeZoneID, sep=": ")
            #print("timeZoneName", self.timeZoneName, sep=": ")
        except:
            print("無法取得offset ")
        return self.rawOffset
            
    def info(self):
        #location
        print("地點全稱：", self.address)
        print("lat:", self.lat)
        print("lng:", self.lng, "\n")
        #timeoffset
        print("rawOffset", self.rawOffset, sep=": ")
        print("timeZoneID", self.timeZoneID, sep=": ")
        print("timeZoneName", self.timeZoneName, sep=": ")
    
    def get_timezone_info(self):
        print("地點全稱：", self.address)
        print("rawOffset", self.rawOffset, sep=": ")
        print("timeZoneID", self.timeZoneID, sep=": ")
        print("timeZoneName", self.timeZoneName, sep=": ")

class Timezone_google_api:
    
    def __init__(self, year, month, day, lat, lng):
        self.date = str(year)+"-"+str(month)+"-"+str(day) #date format: YYYY-MM-DD
        self.lat = str(lat)
        self.lng = str(lng)
        self.formatted = str(0) #不進行格式處理，以方便後續處理

    def get(self):
        url = "https://api.sunrise-sunset.org/json?lat="+self.lat+"&lng="+self.lng+"&date="+self.date+"&formatted="+self.formatted
        json_data = urlopen(url).read().decode("utf8")
        try:
            jsonObj = json.loads(json_data)

            sunrise_time_str = jsonObj.get("results").get("sunrise")
            sunset_time_str = jsonObj.get("results").get("sunset")
            #print("日出時間(UTC):", sunrise_time_str)
            #print("日落時間(UTC):", sunset_time_str)

            import datetime #處理時間用
            sunrise_time = datetime.datetime.strptime(sunrise_time_str, "%Y-%m-%dT%H:%M:%S+00:00")
            sunset_time = datetime.datetime.strptime(sunset_time_str, "%Y-%m-%dT%H:%M:%S+00:00")
            #print("日出時間(UTC): ", sunrise_time)
            #print("日落時間(UTC): ", sunset_time)
        except:
            print("輸入資料出錯")
        return [sunrise_time, sunset_time]