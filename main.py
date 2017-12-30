from info import Get_info #import Get_info class
from formula import Calcular_sunrise_sunset_time

def first_layer_menu():
    print("功能：")
    print("1. 經緯度相關")
    print("2. 時區相關")
    print("3. 日出日落相關")
    print("4. 白天時間相關")
    return input("請輸入你的選擇 (1-4) : ")

#menu
print()
print("這個程式可以用來計算每天的日出日落時間以及每天的白天時間(daytime)")
print("並將daytime在一年的秒數繪畫出來")

#重要variable
location = input("location: ") #儲存位置
api_key_for_geocoding = "AIzaSyBWr7l1Mv_2aFrjx2OTwVBmS78L5Dtfruo" #使用google api 的 token
language = "zh-TW" #return 的 json的資料為正體中文
api_key_for_timezone = "AIzaSyBWr7l1Mv_2aFrjx2OTwVBmS78L5Dtfruo"

user_opition = first_layer_menu()
if user_opition == 1:
    print("1")
elif user_opition == 2:
    print("2")
elif user_opition == 3:
    print("3")
elif user_opition == 4:
    print("4")



'''
i = Get_info(location, api_key_for_geocoding, language, api_key_for_timezone)
i.get_lat_lng()
i.time_off_set()
i.info()

#pass value
latitude = i.lat
longitude = i.lng
raw_offset = i.time_off_set() / 3600


year = 1990
month = 6
day = 25
#latitude = 40.9
#longitude = -74.3
zenith = 90 + (50 / 60)
c = Calcular_sunrise_sunset_time(year, month, day, latitude, longitude, zenith)
c.calcular_sun_rise_and_set_time("sunrise")
print(c.utc_offset(raw_offset))
print()
c.calcular_sun_rise_and_set_time("sunset")
print(c.utc_offset(raw_offset))
'''