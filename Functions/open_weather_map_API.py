#Open Weather Map API
import os, json, requests


apiKey = os.environ["OPEN_WEATHER_MAP_API_KEY"]
requestSting = "https://api.openweathermap.org/data/2.5/weather?" + "q=London,u" + "k&appid=" + apiKey
weatherData = requests.get(requestSting)

if (weatherData.status_code == requests.codes.ok):
    #The request was completed without errors
    weatherData = json.loads(weatherData.text)
    for info in weatherData:
        print(info)