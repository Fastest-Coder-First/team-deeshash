import requests
import json
import sys
from datetime import datetime, timedelta


api_key  = "5be3db1b048f20e0913cf906987fe4d3"

def get_current_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    temperature = data['main']['temp']
    status = data['weather'][0]['description']
    return temperature, status



def get_hourly_weather(lat,lon):
    hourly_weather = []
    hoururl = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&cnt=10&units=metric&appid={api_key}"
    response = requests.get(hoururl)
    data = response.json()
    for item in data.get("list", []):
        item_time = datetime.strptime(item.get("dt_txt"), "%Y-%m-%d %H:%M:%S")
        temperature = item.get("main", {}).get("temp")
        status = item.get("weather", [{}])[0].get("description")

        hourly_weather.append({"time": item_time, "temperature": temperature, "status": status})

    return hourly_weather

def get_tomorrow_weather(lat,lon):
    tomorrowurl = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&cnt=10&units=metric&appid={api_key}"
    response = requests.get(tomorrowurl)
    data = response.json()
    temperature = None
    presentday = datetime.now()
    rounded_hour = (presentday.hour // 3) * 3
    rounded_time = presentday.replace(hour=rounded_hour, minute=0, second=0, microsecond=0)
    tomorrow = rounded_time + timedelta(days=1)

    for item in data.get("list", []):
        item_time = datetime.strptime(item.get("dt_txt"), "%Y-%m-%d %H:%M:%S")
        if item_time.date() == tomorrow.date() and item_time.hour == rounded_hour:
            temperature = item.get("main", {}).get("temp")
            status = item.get("weather", [{}])[0].get("description")
            break
    return temperature, status, tomorrow.time()

def get_latlong(city):
    geourl = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}"
    response = requests.get(geourl)
    data = response.json()
    if not data:
        print("Enter the correct name")
        return None

    if 'lat' in data[0] and 'lon' in data[0]:
        lat = data[0]['lat']
        lon = data[0]['lon']
        return lat, lon

def colourcode(status):
    if "clear" in status:
        color = "FFE87C"
    elif "cloud" in status:
        color = "c1cad9"
    elif "rain" in status:
        color = "87ceeb"
    ansi_escape = f"\x1b[38;2;0;0;0m\x1b[48;2;{int(color[:2], 16)};{int(color[2:4], 16)};{int(color[4:], 16)}m"
    return ansi_escape


    

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        print("Usage: python weather_cli.py <city_name> [-time <time>] [-verbose] [-help]")
        return
    if len(args) < 1 or "-help" in args:
        print("Usage: python weather_cli.py <city_name> [-time <time>] [-verbose] [-help]")
        return
    city = sys.argv[1]
    lat, lon = get_latlong(city)
    temp, status = get_current_weather(city)

    RESET = "\033[0m"
    if len(args) < 2:
        ansi_escape = colourcode(status)
        print(f"Current Weather: {temp} °C")
        print(f"Current Status: " + ansi_escape + f"{status.title()}" + RESET)
    if "-time" in args:
        time_arg_index = args.index("-time")
        if time_arg_index + 1 < len(args) and args[time_arg_index + 1].lower() == "tomorrow":
            temp, status, rounded_time = get_tomorrow_weather(lat,lon)
            ansi_escape = colourcode(status)
            print(f"Tomorrow's Weather will be {temp} °C at time {rounded_time}")
            print("Tomorrow's Status: " + ansi_escape + f"{status.title()}" + RESET)
        if time_arg_index + 1 < len(args) and args[time_arg_index + 1].lower() == "hourly":
            hourly_weather = get_hourly_weather(lat,lon)

            for weather in hourly_weather:
                status = weather['status']
                ansi_escape = colourcode(status)
                print(f"Time: {weather['time']}")
                print(f"Temperature: {weather['temperature']}°C")
                print(f"Description: " + ansi_escape + f"{status.title()}" + RESET)
                print()


if __name__ == '__main__':
    main()