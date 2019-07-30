#conda activate atlasai && python -m rasa_core_sdk.endpoint --actions actions
# in duckling files stack exec duckling-example-exe

#Enviroment vars are setup in ~/.profile, export varName=varValue

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
import os

def get_var(variable):
    #Check if the enviroment variable exists
    var = os.environ[variable]
    return var

class ActionWeatherReturn(Action):

    def name(self):
        self.actionName = "action_weather_return"
        return self.actionName

    def run(self, dispatcher, tracker, domain):
        import json, requests
        #Make module that generates a log file with error

        trackers = tracker.current_slot_values()
        if tracker.get_slot('location') == None:
            location = "Puerto Rico"
        else:
            location = tracker.get_slot('location')
        
        #Keep enclosed to reduce random errors
        try:
            apiKey = get_var("OPEN_WEATHER_MAP_API_KEY")
            tempUnit = "Celcius" #Temp unit might change depending request

            
            requestType = "forecast"

            #Ugly try catch for checking which format added
            timeString = "today"
            try:
                time_command = tracker.get_slot('time')[0][:-6]
                threshold = 0
            except:
                pass
            try:
                time_command = tracker.get_slot('time')[0]['to'][:-6]
                threshold = -1
            except:
                pass
            try: #enclose time request, if it failt it doesnt fail the whole request
                print(time_command)
                from datetime import datetime, timezone
                #Compare current time with requested time
                time_command = int(datetime.strptime(time_command,"%Y-%m-%dT%H:%M:%S.%f").timestamp() / 86400) + threshold
                time_current = int(datetime.now(timezone.utc).timestamp() / 86400)
                print(f"Asked time in days {time_command}")
                print(f"Today's time in days {time_current}")

                #Time related concistency for return sentence
                time_difference = time_command - time_current
                if (time_current <= time_command) and (time_difference <= 5):
                    if time_difference == 1:
                        timeString = "tomorrow"
                    elif (time_difference > 1) and (time_difference <= 5):
                        timeString = f"in {time_difference} days"
                else:
                    requestType = "error"
                
            except Exception as e:
                time_difference = 0
                print(e)

            if requestType == "error":
                #If requesting wrong date
                print("User input time not allowed in api")
                dispatcher.utter_message("The A P I allowed forecast time is from today to the next 5 days.")

            else:
                #Build string and get the slot values
                requestSting = f"https://api.openweathermap.org/data/2.5/{requestType}?q={location}&units={tempUnit}&appid={apiKey}"
                weatherData = requests.get(requestSting)
                weather_arg = tracker.get_slot('weather_arg') #gets the slot value
                trackers = tracker.current_slot_values()
                print("Weather Args: ", weather_arg)
                print("trackers ", trackers)

                if (weatherData.status_code == requests.codes.ok):#If the request is good
                    weatherData = json.loads(weatherData.text)
                    
                    #Response dictionary build
                    returnDic = {"default":"", "rain":"", "quantity":"", "temp":"", "humidity":"", "clowdy":""}
                    if requestType == "forecast":
                        weatherData = weatherData['list'][time_difference]
                    returnDic['default'] = f"You will be experiencing {weatherData['weather'][0]['description'].lower()}"
                    if weather_arg is not None:
                        for arg in weather_arg:
                            if arg == "rain":
                                try:
                                    returnDic[arg] = f"up to {weatherData['rain']['1h']} milileters of rain"
                                    if "quantity" not in weather_arg:
                                        returnDic[arg] = "rain"
                                except:
                                    returnDic[arg] = "no rain"
                            if arg == "temp":
                                if "metric" in weather_arg:
                                    tempUnit = "Celcius"
                                elif "imperial" in weather_arg:
                                    tempUnit = "Fahrenheit"
                                returnDic[arg] = f"temperatures of {weatherData['main']['temp']} {tempUnit}"
                            if arg == "wind":
                                eturnDic[arg] = f"a wind speed of {weatherData['wind']['speed']} miles per hour"
                            if arg == "humidity":
                                returnDic[arg] = f"a humidity of {weatherData['main']['humidity']} percent" #TODO: humidity verbal descriptors
                            if arg == "clowdy":
                                returnDic[arg] = f"a clowdiness of {weatherData['clouds']['all']} percent" #TODO: humidity verbal descriptors111
                            if arg == "snowing":
                                try:
                                    returnDic[arg] = f"up to {weatherData['snow']['1h']} milileters of rain"
                                    if "quantity" not in weather_arg:
                                        returnDic[arg] = "snow"
                                except:
                                    returnDic[arg] = "no snow"
                            


                    returnString = f"{returnDic['default']} with {returnDic['rain']} {returnDic['quantity']} {returnDic['temp']} {returnDic['humidity']} {returnDic['clowdy']} {timeString} in {location}"
                
                dispatcher.utter_message(f"{returnString}")

        except Exception as e:
            print(e)
            dispatcher.utter_message(f"Could not connect to Open Weather Map services!")

class ActionWeatherReturn(Action):

    def name(self):
        self.actionName = "action_reminder_set"
        return self.actionName

    def run(self, dispatcher, tracker, domain):
        trackers = tracker.current_slot_values()
        print("trackers ", trackers)