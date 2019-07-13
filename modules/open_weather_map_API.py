import os, json, requests

def request_Weather(location, requestType, apiKey): 
    """
    Request weather string to read out loud.

    Args:
        location: From where to ask for forecast.
        requestType: Ask for either 'weather' or 'forecast'.
        NOTE: the free version only allows:
            * Current weather data
            * 5 day / 3 hour forecast

    Returns:
        Forecast string, api key error or connection error.
    """
    #TODO: if a date is requested ask forecast, if not weather
    
    #Check if a connection to the API is present
    try:
        requestSting = "https://api.openweathermap.org/data/2.5/" + requestType + "?" + "q=" + location + "&units=metric" + "&appid=" + apiKey 
        weatherData = requests.get(requestSting)
    except:
        return 'Could not connect to Open Weather Map services!'

    #Make the string varie between dates and so forth
    if (weatherData.status_code == requests.codes.ok):
        #The request was completed without errors
        weatherData = json.loads(weatherData.text)   
        try:
            rainString =  f" with a potential rain volume of {weatherData ["rain"]["3h"]} milimiters"
        except KeyError:
            rainString = ""

        returnString = f"Today you will be experiencing {weatherData["weather"][0]["main"].lower()}, the temperature is {weatherData["main"]["temp"]} Celcius with a humidity of {weatherData["main"]["humidity"]} percent"

        returnString += rainString + "."

        #for key, keyData in weatherData.items():
            #print("{key} : {keyData}")
        return returnString

if __name__ == "__main__":
    print(request_Weather("Puerto Rico", "weather"))