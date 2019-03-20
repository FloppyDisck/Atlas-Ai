#Open Weather Map API
import os, json, requests

#requestType = ["weather", "forecast"]

def request_Weather(location, requestType): #if a date is requested ask forecast, if not weather
    apiKey = os.environ["OPEN_WEATHER_MAP_API_KEY"]
    location = "Puerto Rico"
    requestSting = "https://api.openweathermap.org/data/2.5/" + requestType + "?" + "q=" + location + "&units=metric" + "&appid=" + apiKey 
    weatherData = requests.get(requestSting)
    #Make the string varie between dates and so forth
    if (weatherData.status_code == requests.codes.ok):
        #The request was completed without errors
        weatherData = json.loads(weatherData.text)   
        try:
            rainString =  " with a potential rain volume of {} milimiters".format(weatherData ["rain"]["3h"])
        except KeyError:
            rainString = ""
        returnString = "Today you will be experiencing {}, the temperature is {} Celcius with a humidity of {} percent".format(
            weatherData["weather"][0]["main"].lower(), weatherData["main"]["temp"], weatherData["main"]["humidity"])

        returnString += rainString + "."

        #for key, keyData in weatherData.items():
            #print("{} : {}".format(key, keyData))
        return returnString

if __name__ == "__main__":
    print(request_Weather("Puerto Rico", "weather"))