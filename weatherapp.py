from flask import Flask, request, render_template
import requests
from datetime import datetime, timedelta


API_KEY = "5be3db1b048f20e0913cf906987fe4d3"

app = Flask(__name__)

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        temperature = data['main']['temp']
        status = data['weather'][0]['description']
        return temperature, status
    else:
        return None, None

def get_tomorrow_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        tomorrow = datetime.now() + timedelta(days=1)
        for item in data.get("list", []):
            item_time = datetime.strptime(item.get("dt_txt"), "%Y-%m-%d %H:%M:%S")
            if item_time.date() == tomorrow.date():
                temperature = item.get("main", {}).get("temp")
                status = item.get("weather", [{}])[0].get("description")
                return temperature, status
        return None, None
    else:
        return None, None

def get_hourly_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&cnt=10&units=metric&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        hourly_weather = []
        for item in data.get("list", []):
            item_time = datetime.strptime(item.get("dt_txt"), "%Y-%m-%d %H:%M:%S")
            temperature = item.get("main", {}).get("temp")
            status = item.get("weather", [{}])[0].get("description")
            hourly_weather.append({"time": item_time, "temperature": temperature, "status": status})
        return hourly_weather
    else:
        return []

@app.route('/', methods=['GET', 'POST'])
def home():
    city = None
    temperature = None
    status = None
    tomorrow_temperature = None
    tomorrow_status = None
    hourly_weather = []

    if request.method == 'POST':
        city = request.form['city']
        if 'current_weather' in request.form:
            temperature, status = get_weather(city)
        if 'tomorrow_weather' in request.form:
            tomorrow_temperature, tomorrow_status = get_tomorrow_weather(city)
        if 'hourly_weather' in request.form:
            hourly_weather = get_hourly_weather(city)

    return render_template('index.html', city=city, temperature=temperature, status=status,
                           tomorrow_temperature=tomorrow_temperature, tomorrow_status=tomorrow_status,
                           hourly_weather=hourly_weather)

if __name__ == '__main__':
    app.run(debug=True)