# -*- coding: utf-8 -*-
from math import *
import datetime #用作處理時間用

class Calcular_sunrise_sunset_time:
    def __init__(self, year, month, day, latitude, longitude, zenith = 90 + (50 / 60)):
        '''
        特別注意
        zenith:     #Sun's zenith for sunrise/sunset
            offical      = 90 degrees 50'
            civil        = 96 degrees
            nautical     = 102 degrees
            astronomical = 108 degrees
        '''
        self.year = year
        self.month = month
        self.day = day
        self.latitude = latitude
        self.longitude = longitude
        self.zenith = zenith
    
    def calcular_sun_rise_and_set_time(self, opition):
        #the_day_of_year
        N1 = floor(275 * self.month / 9)
        N2 = floor((self.month + 9) / 12)
        N3 = (1 + floor((self.year - 4 * floor(self.year / 4) + 2) /3))
        N = N1 - (N2 * N3) + self.day - 30
        self.the_day_of_year_result = N
        #calculate_approximate_time
        #print("the_day_of_year_value", self.the_day_of_year_result, sep = ": ")
        lngHour = self.longitude / 15
        if opition == "sunrise":
            self.calculate_approximate_time_result = self.the_day_of_year_result + ((6 - lngHour) / 24)
        elif opition == "sunset":
            self.calculate_approximate_time_result = self.the_day_of_year_result + ((18 - lngHour) / 24)
        else:
            print("輸入錯誤argument")
        #print("calculate_approximate_time_result", self.calculate_approximate_time_result, sep = ": ")
        #sun_anomaly
        M = (0.9856 * self.calculate_approximate_time_result) - 3.289
        self.sun_anomaly_result = M
        #print("sun_anomaly_result", self.sun_anomaly_result, sep = ": ")
        #sun_true_longitude
        L = self.sun_anomaly_result + (1.916 * sin(self.sun_anomaly_result * pi / 180)) + (0.020 * sin(2 * self.sun_anomaly_result * pi / 180)) + 282.634
        L = L - int(L / 360) * 360 #make sure return value in the range [0,360)
        self.sun_true_longitude_result = L
        #print("sun_true_longitude_result", self.sun_true_longitude_result, sep = ": ")
        #sun_right_ascension
        RA = atan(0.91764 * tan(self.sun_true_longitude_result * pi / 180)) * 180 / pi
        RA = RA - int(RA / 360) * 360
        self.sun_right_ascension_result = RA
        #print("sun_right_ascension_result", self.sun_right_ascension_result, sep = ": ")
        #same_quadrant
        sun_true_longitude_result_quadrant = (floor(self.sun_true_longitude_result / 90)) * 90
        sun_right_ascension_result_quadrant = (floor(self.sun_right_ascension_result / 90)) * 90
        sun_right_ascension_result = self.sun_right_ascension_result + (sun_true_longitude_result_quadrant - sun_right_ascension_result_quadrant)
        self.same_quadrant_result = sun_right_ascension_result
        #print("same_quadrant_result", self.same_quadrant_result, sep = ": ")
        #right_ascension_converted_hours
        same_quadrant_result = self.same_quadrant_result / 15
        self.same_quadrant_result = same_quadrant_result
        #print("same_quadrant_result_", self.same_quadrant_result, sep = ": ")
        #sun_declination
        sinDec = 0.39782 * sin(self.sun_true_longitude_result * pi / 180)
        cosDec = cos((asin(sinDec) * 180 / pi) * pi / 180 )
        #sun_local_hour_angle
        cosH = (cos(self.zenith * pi / 180) - (sinDec * sin(self.latitude * pi / 180))) / (cosDec * cos(self.latitude * pi / 180))
        if cosH > 1:
            print("the sun never rises on this location (on the specified date)")
        elif cosH < - 1:
            print("the sun never sets on this location (on the specified date)")
        self.sun_local_hour_angle_result = cosH
        #print("sun_local_hour_angle_result", self.sun_local_hour_angle_result, sep = ": ")
        #h_convert_hours
        if opition == "sunrise":
            H = 360 - acos(self.sun_local_hour_angle_result) * 180 / pi
        elif opition == "sunset":
            H = acos(self.sun_local_hour_angle_result) * 180 / pi
        H = H / 15
        self.h_convert_hours_result = H
        #print("h_convert_hours_result", self.h_convert_hours_result, sep = ": ")
        #local_mean_time
        T = self.h_convert_hours_result + self.same_quadrant_result - (0.06571 * self.calculate_approximate_time_result) - 6.622
        self.local_mean_time_result = T
        #print("local_mean_time_result", self.local_mean_time_result, sep = ": ")
        #convert_utc
        UT = self.local_mean_time_result - self.longitude / 15
        UT = UT - int(UT / 24) * 24
        utc_hour = int(UT / 1)
        utc_minute = UT % 1
        if utc_hour < 0:
            utc_hour += 24
        self.utc_hour = utc_hour
        self.utc_minute = int(utc_minute * 60)
        self.utc_second = (utc_minute * 60 % 1) * 60
        #self.time_result_str = str(self.year)+"-"+str(self.month)+"-"+str(self.day)+" "+str(self.utc_hour)+":"+str(self.utc_minute)+":"+str(int(self.utc_second)) #在main.py會造成day 出錯
        #self.time_result = datetime.datetime.strptime(self.time_result_str, "%Y-%m-%d %H:%M:%S")
        self.time_result_str = str(self.utc_hour)+":"+str(self.utc_minute)+":"+str(int(self.utc_second))
        self.time_result = datetime.datetime.strptime(self.time_result_str, "%H:%M:%S")
        return self.time_result


    '''
    def utc_offset(self, offset_value):
        utc_hour = self.utc_hour
        utc_hour += offset_value
        if utc_hour < 0:
            utc_hour = utc_hour + 24
        elif utc_hour >= 24:
            utc_hour = utc_hour - 24
        return [utc_hour, self.utc_minute] #return 的 utc minute 未轉換為 60 進制
    '''

'''
year = 1990
month = 6
day = 25
latitude = 40.9
longitude = -74.3
zenith = 90 + (50 / 60)
c = Calcular_sunrise_sunset_time(year, month, day, latitude, longitude, zenith)
c.calcular_sun_rise_and_set_time("sunrise")
print(c.utc_offset(8))
print()
c.calcular_sun_rise_and_set_time("sunset")
print(c.utc_offset(8))
'''
