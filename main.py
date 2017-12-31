from info import Get_info #取得資訊
from info import Timezone_google_api #用google api 取得日出日落時間
from formula import Calcular_sunrise_sunset_time #use Calcular_sunrise_sunset_time class
import datetime #處理時間用
import pylab

def first_layer_menu():
    print("功能：")
    print("1. 經緯度相關 (列出輸入地點的經緯度)")
    print("2. 時區相關 (列出與時區相關的資訊)")
    print("3. 日出日落相關 (使用Google 提供的 API)")
    print("4. 日出日落相關 (使用參考的公式計算)")
    print("5. 計算daytime (輸出白天長度)")
    print("6. 輸出特定時間內的 daytime 秒數之間關係的圖形")
    print() #Line feed
    return int(input("請輸入你的選擇 (1-4) : "))

def second_layer_menu_opition_1():
    print("列出經緯度")
    i = Get_info(location, api_key_for_geocoding, language, api_key_for_timezone)
    print("latitude: ", i.get_lat_lng()[0], "longitude: ", i.get_lat_lng()[1])

def second_layer_menu_opition_2():
    print("列出時區相關資訊")
    i = Get_info(location, api_key_for_geocoding, language, api_key_for_timezone)
    i.get_lat_lng()
    i.time_off_set()
    i.get_timezone_info()

def second_layer_menu_opition_3():
    print("列出日出日落時間 (從Google API)")
    year = int(input("輸入年份（西元）："))
    month = int(input("輸入月份："))
    day = int(input("輸入日期："))
    i = Get_info(location, api_key_for_geocoding, language, api_key_for_timezone)
    t = Timezone_google_api(year, month, day, i.get_lat_lng()[0], i.get_lat_lng()[1])
    i.time_off_set()
    #prepare timeoffset
    sunrise_sunset_tim = t.get()
    sunrise = sunrise_sunset_tim[0]
    sunset = sunrise_sunset_tim[1]
    #timeoffset
    timeoffset = i.time_off_set() #second
    sunrise = sunrise + datetime.timedelta(seconds = int(timeoffset))
    sunset = sunset + datetime.timedelta(seconds = int(timeoffset))
    print("日出時間(local time): ", sunrise)
    print("日落時間(local time): ", sunset)

def second_layer_menu_opition_4(year, month, day, zenith):
    #取得經緯度
    i = Get_info(location, api_key_for_geocoding, language, api_key_for_timezone)
    latitude = i.get_lat_lng()[0]
    longitude = i.get_lat_lng()[1]
    #取得 zenith
    
    c = Calcular_sunrise_sunset_time(year, month, day, latitude, longitude, zenith)
    sunrise = c.calcular_sun_rise_and_set_time("sunrise")
    sunset = c.calcular_sun_rise_and_set_time("sunset")
    #timeoffset
    i = Get_info(location, api_key_for_geocoding, language, api_key_for_timezone)
    t = Timezone_google_api(year, month, day, i.get_lat_lng()[0], i.get_lat_lng()[1])
    timeoffset = i.time_off_set() #second
    sunrise = sunrise + datetime.timedelta(seconds = int(timeoffset))
    sunset = sunset + datetime.timedelta(seconds = int(timeoffset))
    sunrise_result_str = str(year)+"-"+str(month)+"-"+str(day)+" "+str(sunrise.hour)+":"+str(sunrise.minute)+":"+str(sunrise.second)
    sunset_result_str = str(year)+"-"+str(month)+"-"+str(day)+" "+str(sunset.hour)+":"+str(sunset.minute)+":"+str(sunset.second)
    sunrise = datetime.datetime.strptime(sunrise_result_str, "%Y-%m-%d %H:%M:%S")
    sunset = datetime.datetime.strptime(sunset_result_str, "%Y-%m-%d %H:%M:%S")
    #print("日出時間(local time): ", sunrise)
    #print("日落時間(local time): ", sunset)
    return [sunrise, sunset]

def second_layer_menu_opition_5(sunrise_sunset_time):
    sunrise_to_second = sunrise_sunset_time[0].hour * 3600 + sunrise_sunset_time[0].minute * 60 + sunrise_sunset_time[0].second
    sunset_to_second = sunrise_sunset_time[1].hour * 3600 + sunrise_sunset_time[1].minute * 60 + sunrise_sunset_time[1].second
    second = sunset_to_second - sunrise_to_second
    minute = (sunset_to_second - sunrise_to_second) / 60
    hour = (sunset_to_second - sunrise_to_second) / 3600
    return [hour, minute, second]

#draw picture
def second_layer_menu_opition_6(result):
    xs = []
    for x in range(len(result)):
        xs += [x]
        #print("xs: ", xs[x], " ys: ", result[x])
    pylab.plot(xs, result)
    pylab.show()
    

#menu
print("這個程式可以用來計算每天的日出日落時間以及每天的白天時間(daytime)")
print("並將daytime在一年的秒數繪畫出來\n")

#重要variable
location = input("請輸入您想查詢的地點 （如想查詢特定經緯度只需直接輸入）: ") #儲存位置
api_key_for_geocoding = "AIzaSyBWr7l1Mv_2aFrjx2OTwVBmS78L5Dtfruo" #使用google api 的 token
language = "zh-TW" #return 的 json的資料為正體中文
api_key_for_timezone = "AIzaSyBWr7l1Mv_2aFrjx2OTwVBmS78L5Dtfruo"

hr = "-" * 50

user_opition = first_layer_menu()
print() #line feed
if user_opition == 1:
    #print("1")
    print(hr)
    second_layer_menu_opition_1()
elif user_opition == 2:
    #print("2")
    print(hr)
    second_layer_menu_opition_2()
elif user_opition == 3:
    #print("3")
    print(hr)
    second_layer_menu_opition_3()
elif user_opition == 4:
    #print("4")
    print("列出日出日落時間 (使用參考的公式計算)")
    year = int(input("輸入年份（西元）："))
    month = int(input("輸入月份："))
    day = int(input("輸入日期："))
    print() #Line feed
    print("Hint: ")
    print("在各位領域中的 zenith(頂點) 皆不相同")
    print("Offical zeinth is 90 degrees 50' \ncivil zeinth is 96 degrees \nnautical zeinth is 102 degrees \nastronomical zeinth is 108 degrees")
    zenith = input("結果沒有輸入數值default value是[90 degrees 50']: ")
    if zenith == "":
        #print("沒有輸入zenith value")
        zenith = 90 + (50 / 60)
    print() #Line feed
    result = second_layer_menu_opition_4(year, month, day, zenith)
    print("日出時間(local time): ", result[0])
    print("日落時間(local time): ", result[1])
    print(hr)
elif user_opition == 5:
    print("計算白天長度(daytime)")
    year = int(input("輸入年份（西元）："))
    month = int(input("輸入月份："))
    day = int(input("輸入日期："))
    print() #Line feed
    print("Hint: ")
    print("在各位領域中的 zenith(頂點) 皆不相同")
    print("Offical zeinth is 90 degrees 50' \ncivil zeinth is 96 degrees \nnautical zeinth is 102 degrees \nastronomical zeinth is 108 degrees")
    zenith = input("結果沒有輸入數值default value是[90 degrees 50']: ")
    if zenith == "":
        #print("沒有輸入zenith value")
        zenith = 90 + (50 / 60)
    print() #Line feed
    result = second_layer_menu_opition_5(second_layer_menu_opition_4(year, month, day, zenith))
    print("daytime 為 (hour): ", result[0], " 小時 (hour)")
    print("daytime 為 (minute): ", result[1], " 分鐘 (minute)")
    print("daytime 為 (second): ", result[2], " 秒 (second)")
    print(hr)
elif user_opition == 6:
    print("輸入開始時間")
    start_year = int(input("輸入年份（西元）："))
    start_month = int(input("輸入月份："))
    start_day = int(input("輸入日期："))
    start_date = datetime.datetime(start_year, start_month, start_day)
    var_date = start_date
    print()
    print("輸入結束時間")
    end_year = int(input("輸入年份（西元）："))
    end_month = int(input("輸入月份："))
    end_day = int(input("輸入日期："))
    end_date = datetime.datetime(end_year, end_month, end_day)
    result = []
    max_date = var_date
    min_date = var_date
    max_value = 0
    min_value = 999999999999999999999999
    while(not (var_date.date() == end_date.date()) ):
        var_date = var_date + datetime.timedelta(days = 1)
        year = var_date.year
        month = var_date.month
        day = var_date.day
        zenith = 90 + (50 / 60)
        arr = second_layer_menu_opition_5(second_layer_menu_opition_4(year, month, day, zenith))[2]
        if arr > max_value:
            max_value = arr
            max_date = var_date
        elif arr < min_value:
            min_value = arr
            min_date = var_date
        result += [arr]
        print("date: ", var_date, " result: ", arr)
    print("daytime 最大時間: ", max_date, " 秒數為: ", max_value)
    print("daytime 最小時間", min_date, " 秒數為: ", min_value)
    second_layer_menu_opition_6(result)
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