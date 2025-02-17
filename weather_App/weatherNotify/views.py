from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests 
from bs4 import BeautifulSoup 
from win10toast import ToastNotifier
from datetime import datetime , timedelta 
import pytz 


# Create your views here.
def index(request):
    CITY = "London"
    API_KEY = "bea2c0b0da516012b3bb96c7d753f1d5"
    
    
    
    if request.method == "POST": 
        CITY = request.POST.get("city","London")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url) 
    data = response.json() 
    
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"
    forecast_response = requests.get(forecast_url) 
    forecast_data = forecast_response.json() 
    
    
    error_m = None 
    
    if data.get("cod") == 200: 
        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]
        pressure = data["main"]["pressure"]
        rain = data.get("rain", {}).get("1h", 0)
        timezone = data.get("timezone",0) 
        
        utc_time = datetime.utcfromtimestamp(data["dt"])
        
        local_time = utc_time + timedelta(seconds=timezone)
        
        year = local_time.year 
        month = local_time.month 
        day = local_time.day 
        hour = local_time.hour 
        minute = local_time.minute
        if 0 < minute < 10: 
            minute = "0" + str(minute)
        if 0 < month < 10: 
            month = "0" + str(month)
        # Get sunrise and sunset times
        sunrise = datetime.utcfromtimestamp(data["sys"]["sunrise"]) + timedelta(seconds=timezone)
        sunset = datetime.utcfromtimestamp(data["sys"]["sunset"]) + timedelta(seconds=timezone)
        
        # Check if it's dark outside
        is_dark = local_time < sunrise or local_time > sunset
        
        #current
        rainImg = False #done
        sunImg = False 
        moonImg = False 
        snowImg = False #done
        sunBehindCloud = False 
        moonBehindCloud = False 
    
        if rain != 0: 
            rainImg = True
        elif weather.find("snow"):
            snowImg = True 
        elif weather.find("clouds") and is_dark: 
            moonBehindCloud = True 
        elif weather.find("clouds") and not is_dark: 
            SunBehindClouds = True 
        elif is_dark: 
            moonImg = True 
        elif not is_dark: 
            sunImg = True
        

 
        
        

    else: 
        temp = "N/A"
        weather = "N/A" 
        wind_speed = "N/A" 
        pressure = "N/A" 
        rain = "N/A" 
        year = "N/A"
        month = "N/A"
        day = "N/A"  
        hour = "N/A"
        minute = "N/A"
        todays_forecast= [] 
        weeks_forecast = [] 
        todaysImg = [] 
        weekImg = []
        rainImg = None 
        snowImg = None 
        moonBehindCloud = None 
        sunBehindCloud = None 
        moonImg = None 
 
        sunImg = None 
        is_dark = False
    
    forecast_list = [] 
    if forecast_data.get("cod") == "200":
        for item in forecast_data["list"]:
            forecast_time = datetime.utcfromtimestamp(item["dt"]) + timedelta(seconds=timezone)
            forecast_list.append({
                "date": forecast_time.strftime("%Y-%m-%d"),
                "time": forecast_time.strftime("%H:%M"),
                "temp": item["main"]["temp"],
                "weather": item["weather"][0]["description"],
                "wind_speed": item["wind"]["speed"],
                "pressure": item["main"]["pressure"],
                "rain": item.get("rain", {}).get("3h", 0),
            })
        todays_forecast = []
        weeks_forecast = []
        dateHolder = []
        #print(type(forecast_list[0]["date"]))
        for i in range(6):
            
            todays_forecast.append(forecast_list[i])
        for i in range(7,40):
            if forecast_list[i]["date"] in dateHolder:
                pass
            else:
                dateHolder.append(forecast_list[i]["date"])
                weeks_forecast.append(forecast_list[i])
        
        print(len(forecast_list))

        
        
        todaysImg = []
        for i in range(len(todays_forecast)):
            if todays_forecast[i]["rain"] != 0:
                todaysImg.append("rain")
            elif todays_forecast[i]["weather"].find("snow"):
                todaysImg.append("snow")
            elif todays_forecast[i]["weather"].find("clouds") and is_dark: 
                todaysImg.append("darkClouds")
            elif todays_forecast[i]["weather"].find("clouds") and not is_dark: 
                todaysImg.append("sunClouds")
            elif is_dark: 
                todaysImg.append("dark")
            elif not is_dark: 
                todaysImg.append("sun")
        
        
        j = 0
        weekImg = []
        for i in range(len(weeks_forecast)):
            if weeks_forecast[i]["date"] in dateHolder:
                j += 1
                pass
            else:
                
                dateHolder.append(weeks_forecast[i]["date"])
                if weeks_forecast[j]["rain"] != 0: 
                    weekImg.append("rain")
                elif weeks_forecast[j]["weather"].find("snow"):
                    weekImg.append("snow")
                elif weeks_forecast[j]["weather"].find("clouds") and is_dark:
                    weekImg.append("darkClouds")
                elif weeks_forecast[j]["weather"].find("clouds") and not is_dark:
                    weekImg.append("sunClouds")
                elif is_dark:
                    weekImg.append("dark")
                elif not is_dark:
                    weekImg.append("sun")
                j += 1
                    

    
    return render(request,"frame/frame.html",{
            "year": year, 
            "month": month, 
            "day": day, 
            "hour": hour, 
            "minute": minute, 
            
            "temp": temp,
            "CITY": CITY, 
            "weather": weather, 
            "wind": wind_speed, 
            "pressure": pressure, 
            "rain": rain,
            
            "forecast_list": forecast_list,
            "todays_forecast": todays_forecast,
            "weeks_forecast": weeks_forecast,
            
            "rainImg": rainImg,
            "snowImg": snowImg, 
            "moonBehingCloud": moonBehindCloud, 
            "sunBehindCloud": sunBehindCloud, 
            "moonImg": moonImg, 
            "sunImg": sunImg,
            
            "todaysImg": todaysImg, 
            "weekImg": weekImg,
            
            "is_dark": is_dark,

        })

'''
now = datetime.datetime.now() 
year = now.year 
month = now.month 
day = now.day
hour = now.hour 
minute = now.minute
secs = now.second

CITY = "Waterloo,CA"  # Change to your city

API_KEY = "bea2c0b0da516012b3bb96c7d753f1d5"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(URL)
data = response.json()

if response.status_code == 200:
    temp = data["main"]["temp"]
    weather = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]  # Humidity percentage
    wind_speed = data["wind"]["speed"]  # Wind speed in m/s
    pressure = data["main"]["pressure"]  # Atmospheric pressure in hPa  
    rain = data.get("rain", {}).get("1h", 0)  # Rain in last 1 hour (mm), default to 0 if not available 
else:
    print("Error fetching weather data")
'''

