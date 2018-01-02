
# 計算日出日落時間
參考了[Sunrise/Sunset Algorithm](http://www.edwilliams.org/sunrise_sunset_algorithm.htm) 及 [Sunrise/Sunset Algorithm Example](http://www.edwilliams.org/sunrise_sunset_example.htm)
下方程式碼主要用來計算日出及日落的UTC時間


```python
#input variable
year = 1990
month = 6
day = 25

#latitude, longitude =  40.9, -74.3  #location for sunrise/sunset
latitude, longitude = 24.9936281, 121.3009798
zenith = 0          #Sun's zenith for sunrise/sunset
offical_zeith = 90 + (50 / 60)
#cos_zeith = cos(offical_zeith * pi / 180) #Just for test
#print("cos_zeith: ", cos_zeith)
civil = 96
nautical = 102
astronomical = 108

offset_value = 8 #taiwan is utc+8

from math import *

def the_day_of_year(year, month, day):
    N1 = floor(275 * month / 9)
    N2 = floor((month + 9) / 12)
    N3 = (1 + floor((year - 4 * floor(year / 4) + 2) /3))
    N = N1 - (N2 * N3) + day - 30
    return N

def calculate_approximate_time(longitude, the_day_of_year_result):
    lngHour = longitude / 15
    t_sun_rise = the_day_of_year_result + ((6 - lngHour) / 24)
    t_sun_set = the_day_of_year_result + ((18 - lngHour) / 24)
    return [t_sun_rise, t_sun_set] # First value in the set is sun rise time, and second value is sun set time

def sun_anomaly(calculate_approximate_time_result):
    M = (0.9856 * calculate_approximate_time_result) - 3.289
    return M

def sun_true_longitude(sun_anomaly_result):
    L = sun_anomaly_result + (1.916 * sin(sun_anomaly_result * pi / 180)) + (0.020 * sin(2 * sun_anomaly_result * pi / 180)) + 282.634
    L = L - int(L / 360) * 360 #make sure return value in the range [0,360)
    return L

def sun_right_ascension(sun_true_longitude_result):
    RA = atan(0.91764 * tan(sun_true_longitude_result * pi / 180)) * 180 / pi
    RA = RA - int(RA / 360) * 360
    return RA

def same_quadrant(sun_true_longitude_result, sun_right_ascension_result):
    sun_true_longitude_result_quadrant = (floor(sun_true_longitude_result / 90)) * 90
    sun_right_ascension_result_quadrant = (floor(sun_right_ascension_result / 90)) * 90
    sun_right_ascension_result = sun_right_ascension_result + (sun_true_longitude_result_quadrant - sun_right_ascension_result_quadrant)
    return sun_right_ascension_result

def right_ascension_converted_hours(same_quadrant_result):
    same_quadrant_result = same_quadrant_result / 15
    return same_quadrant_result

def sun_declination(sun_true_longitude_result):
    sinDec = 0.39782 * sin(sun_true_longitude_result * pi / 180)
    cosDec = cos((asin(sinDec) * 180 / pi) * pi / 180 )
    return [sinDec, cosDec]

def sun_local_hour_angle(offical_zeith, sun_declination_result, latitude):
    sinDec = sun_declination_result[0]
    cosDec = sun_declination_result[1]
    cosH = (cos(offical_zeith * pi / 180) - (sinDec * sin(latitude * pi / 180))) / (cosDec * cos(latitude * pi / 180))
    if cosH > 1:
        print("the sun never rises on this location (on the specified date)")
    elif cosH < - 1:
        print("the sun never sets on this location (on the specified date)")
    return cosH

def h_convert_hours(sun_local_hour_angle_result, opition): #opition have two opition
    #"r" means sun rise, and "s" means sun set
    if opition == "r":
        H = 360 - acos(sun_local_hour_angle_result) * 180 / pi
    elif opition == "s":
        H = acos(sun_local_hour_angle_result) * 180 / pi
    H = H / 15
    return H

def local_mean_time(h_convert_hours_results, right_ascension_converted_hours_result, calculate_approximate_time_result):
    T = h_convert_hours_results + right_ascension_converted_hours_result - (0.06571 * calculate_approximate_time_result) - 6.622
    return T

def convert_utc(local_mean_time_result, longitude):
    UT = local_mean_time_result - longitude / 15
    UT = UT - int(UT / 24) * 24
    utc_hour = int(UT / 1)
    utc_minute = UT % 1
    if utc_hour < 0:
        utc_hour += 24
    return [utc_hour, utc_minute]

def utc_offset(convert_utc_result, offset_value):
    convert_utc_result[0] += offset_value
    if convert_utc_result[0] >= 24:
        convert_utc_result[0] -= 24
    return convert_utc_result

#用作分隔用
times = 75
horizon = "*" * times
hr = "-" * times

print(horizon)
#print basic info
print("year: ", year, "month: ", month, "day: ", day)
print("latitude: ", latitude, "longitude: ", longitude) 
print(hr)
#calculate the day of year
the_day_of_year_value = the_day_of_year(year, month, day)
print("the_day_of_year_value", the_day_of_year_value, sep = ": ")
print(hr)
#return approximate time
approximate_sun_rise_time_value = calculate_approximate_time(longitude, the_day_of_year_value)[0]
print("approximate_sun_rise_time_value", approximate_sun_rise_time_value, sep = ": ")
approximate_sun_set_time_value = calculate_approximate_time(longitude, the_day_of_year_value)[1]
print("approximate_sun_set_time_value", approximate_sun_set_time_value, sep = ": ")
print(hr)
#calculate sun anomaly
sun_anomaly_sun_rise_time_value = sun_anomaly(approximate_sun_rise_time_value)
print("sun_anomaly_sun_rise_time_value", sun_anomaly_sun_rise_time_value, sep = ": ")
sun_anomaly_sun_set_time_value = sun_anomaly(approximate_sun_set_time_value)
print("sun_anomaly_sun_set_time_value", sun_anomaly_sun_set_time_value, sep = ": ")
print(hr)
#calculate Sun's true longitude
sun_true_longitude_sun_rise_time_value = sun_true_longitude(sun_anomaly_sun_rise_time_value)
print("sun_true_longitude_sun_rise_time_value", sun_true_longitude_sun_rise_time_value, sep = ": ")
sun_true_longitude_sun_set_time_value = sun_true_longitude(sun_anomaly_sun_set_time_value)
print("sun_true_longitude_sun_set_time_value", sun_true_longitude_sun_set_time_value, sep = ": ")
print(hr)
#calculate Sun's right ascension
sun_right_ascension_longitude_sun_rise_time_value = sun_right_ascension(sun_true_longitude_sun_rise_time_value)
print("sun_right_ascension_sun_rise_time_value", sun_right_ascension_longitude_sun_rise_time_value, sep = ": ")
sun_right_ascension_longitude_sun_set_time_value = sun_right_ascension(sun_true_longitude_sun_set_time_value)
print("sun_right_ascension_sun_set_time_value", sun_right_ascension_longitude_sun_set_time_value, sep = ": ")
print(hr)
#same quadrant
same_quadrant_sun_rise_time_value = same_quadrant(sun_true_longitude_sun_rise_time_value, sun_right_ascension_longitude_sun_rise_time_value)
print("same_quadrant_sun_rise_time_value", same_quadrant_sun_rise_time_value, sep = ": ")
same_quadrant_sun_set_time_value = same_quadrant(sun_true_longitude_sun_set_time_value, sun_right_ascension_longitude_sun_set_time_value)
print("same_quadrant_sun_set_time_value", same_quadrant_sun_set_time_value, sep = ": ")
print(hr)
#right ascension value needs to be converted into hours
right_ascension_converted_hours_sun_rise_time_value = right_ascension_converted_hours(same_quadrant_sun_rise_time_value)
print("right_ascension_converted_hours_sun_rise_time_value", right_ascension_converted_hours_sun_rise_time_value, sep = ": ")
right_ascension_converted_hours_sun_set_time_value = right_ascension_converted_hours(same_quadrant_sun_set_time_value)
print("right_ascension_converted_hours_sun_set_time_value", right_ascension_converted_hours_sun_set_time_value, sep = ": ")
print(hr)
#calculate the Sun's declination
sun_declination_sun_rise_time_value = sun_declination(sun_true_longitude_sun_rise_time_value)[1]
print("sun_declination_sun_rise_time_value", sun_declination_sun_rise_time_value, sep = ": ")
sun_declination_sun_set_time_value = sun_declination(sun_true_longitude_sun_set_time_value)[1]
print("sun_declination_sun_set_time_value", sun_declination_sun_set_time_value, sep = ": ")
print(hr)
#calculate the Sun's local hour angle
Sun_local_hour_angle_sun_rise_time_value = sun_local_hour_angle(offical_zeith, sun_declination(sun_true_longitude_sun_rise_time_value), latitude)
print("Sun_local_hour_angle_sun_rise_time_value", Sun_local_hour_angle_sun_rise_time_value, sep = ": ")
Sun_local_hour_angle_sun_set_time_value = sun_local_hour_angle(offical_zeith, sun_declination(same_quadrant_sun_set_time_value), latitude)
print("Sun_local_hour_angle_sun_set_time_value", Sun_local_hour_angle_sun_set_time_value, sep = ": ")
print(hr)
#H and convert into hours
h_convert_hours_sun_rise_time_value = h_convert_hours(Sun_local_hour_angle_sun_rise_time_value, "r")
print("h_convert_hours_sun_rise_time_value", h_convert_hours_sun_rise_time_value, sep = ": ")
h_convert_hours_sun_set_time_value = h_convert_hours(Sun_local_hour_angle_sun_set_time_value, "s")
print("h_convert_hours_sun_set_time_value", h_convert_hours_sun_set_time_value, sep = ": ")
print(hr)
#local_mean_time
local_mean_time_sun_rise_time_value = local_mean_time(h_convert_hours_sun_rise_time_value, right_ascension_converted_hours_sun_rise_time_value, approximate_sun_rise_time_value)
print("local_mean_time_sun_rise_time_value", local_mean_time_sun_rise_time_value, sep = ": ")
local_mean_time_sun_set_time_value = local_mean_time(h_convert_hours_sun_set_time_value, right_ascension_converted_hours_sun_set_time_value, approximate_sun_set_time_value)
print("local_mean_time_sun_set_time_value", local_mean_time_sun_set_time_value, sep = ": ")
print(hr)
#convert to UTC time
convert_utc_sun_rise_time_value = convert_utc(local_mean_time_sun_rise_time_value, longitude)
print("convert_utc_sun_rise_time_value", convert_utc_sun_rise_time_value, sep = ": ")
convert_utc_sun_set_time_value = convert_utc(local_mean_time_sun_set_time_value, longitude)
print("convert_utc_sun_set_time_value", convert_utc_sun_set_time_value, sep = ": ")
print(hr)
#covert to local time
utc_offset_sun_rise_time_value = utc_offset(convert_utc_sun_rise_time_value, offset_value)
print("utc_offset_sun_rise_time_value", utc_offset_sun_rise_time_value, sep = ": ")
utc_offset_sun_set_time_value = utc_offset(convert_utc_sun_set_time_value, offset_value)
print("utc_offset_sun_set_time_value", utc_offset_sun_set_time_value, sep = ": ")
```

    ***************************************************************************
    year:  1990 month:  6 day:  25
    latitude:  24.9936281 longitude:  121.3009798
    ---------------------------------------------------------------------------
    the_day_of_year_value: 176
    ---------------------------------------------------------------------------
    approximate_sun_rise_time_value: 175.91305283388888
    approximate_sun_set_time_value: 176.41305283388888
    ---------------------------------------------------------------------------
    sun_anomaly_sun_rise_time_value: 170.09090487308092
    sun_anomaly_sun_set_time_value: 170.5837048730809
    ---------------------------------------------------------------------------
    sun_true_longitude_sun_rise_time_value: 93.0478399095229
    sun_true_longitude_sun_set_time_value: 93.52471892226038
    ---------------------------------------------------------------------------
    sun_right_ascension_sun_rise_time_value: -86.67919752027603
    sun_right_ascension_sun_set_time_value: -86.15983833890009
    ---------------------------------------------------------------------------
    same_quadrant_sun_rise_time_value: 93.32080247972397
    same_quadrant_sun_set_time_value: 93.84016166109991
    ---------------------------------------------------------------------------
    right_ascension_converted_hours_sun_rise_time_value: 6.221386831981598
    right_ascension_converted_hours_sun_set_time_value: 6.256010777406661
    ---------------------------------------------------------------------------
    sun_declination_sun_rise_time_value: 0.9177072814387344
    sun_declination_sun_set_time_value: 0.9177894222768794
    ---------------------------------------------------------------------------
    Sun_local_hour_angle_sun_rise_time_value: -0.2192822439396342
    Sun_local_hour_angle_sun_set_time_value: -0.2190802354656302
    ---------------------------------------------------------------------------
    h_convert_hours_sun_rise_time_value: 17.155541384218623
    h_convert_hours_sun_set_time_value: 6.843667770173764
    ---------------------------------------------------------------------------
    local_mean_time_sun_rise_time_value: 5.195681514485381
    local_mean_time_sun_set_time_value: -5.114423154134414
    ---------------------------------------------------------------------------
    convert_utc_sun_rise_time_value: [22, 0.10894952781871403]
    convert_utc_sun_set_time_value: [11, 0.798844859198919]
    ---------------------------------------------------------------------------
    utc_offset_sun_rise_time_value: [6, 0.10894952781871403]
    utc_offset_sun_set_time_value: [19, 0.798844859198919]
    

而這個部分則是將日出日落時間轉化為秒
並將日落的秒數減去日出秒數即可得出日照秒數


```python
def daytime_second(sun_rise, sun_set):
    sun_rise_second = sun_rise[0] * 3600 + sun_rise[1] * 60
    sun_set_second = sun_set[0] * 3600 + sun_set[1] * 60
    return sun_set_second - sun_rise_second

#calculate daytime (return value is second)
daytime_value = daytime_second(utc_offset_sun_rise_time_value, utc_offset_sun_set_time_value)
print("daytime_value", daytime_value, sep = ": ")
```

    daytime_value: 46841.39371988282
    
