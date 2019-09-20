# in duckling files stack exec duckling-example-exe
# Enviroment vars are setup in ~/.profile, export varName=varValue

from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import os

def get_var(variable):
    '''Procedure to find enviroment variables.

    API keys must be stored as enviroment variables.
    '''
    try:
        var = os.environ[variable]
        return var
    except:
        return None

class ActionWeatherReturn(Action):

    def name(self):
        self.action_name = "action_weather_return"
        return self.action_name

    def run(self, dispatcher, tracker, domain):
        from custom_actions.action_weather_get import Weather 
        #TODO: Make module that generates a log file with error

        try: # Raise API problem

            trackers = tracker.current_slot_values()
            if tracker.get_slot('location') == None:
                location = "Puerto Rico"
            else:
                location = tracker.get_slot('location')
            
            #Keep enclosed to reduce random errors
            try:
                api_key = get_var("OPEN_WEATHER_MAP_API_KEY")
                temp_unit = "Celcius" #Temp unit might change depending request

            # Get location
            if tracker.get_slot('location') != None:
                weatherReport.location = tracker.get_slot('location')
                
                request_type = "forecast"

                #Ugly try catch for checking which format added
                time_string = "today"
                try:
                    time_command = tracker.get_slot('time')[0][:-6]
                    threshold = 0
                except TypeError:
                    try:  #Different sentence structures lead to different time slots
                        time_command = tracker.get_slot('time')[0]['to'][:-6]
                        threshold = -1
                    except TypeError:
                        time_command = None

                time_difference = 0
                if time_command is not None:  # If last part ran successfully
                    from datetime import datetime, timezone
                    #Compare current time with requested time
                    time_command = int(datetime.strptime(time_command,"%Y-%m-%dT%H:%M:%S.%f").timestamp() / 86400) + threshold
                    time_current = int(datetime.now(timezone.utc).timestamp() / 86400)

                    #Time related concistency for return sentence
                    time_difference = time_command - time_current
                    if (time_current <= time_command) and (time_difference <= 5):
                        if time_difference == 1:
                            time_string = "tomorrow"
                        elif (time_difference > 1) and (time_difference <= 5):
                            time_string = f"in {time_difference} days"
                    else:
                        request_type = "error"
                    
                except Exception as e:
                    time_difference = 0
                    print(e)

                if request_type == "error":
                    #If requesting wrong date
                    print("User input time not allowed in api")
                    dispatcher.utter_message("The A P I allowed forecast time is from today to the next 5 days.")

                else:
                    #Build string and get the slot values
                    request_string = f"https://api.openweathermap.org/data/2.5/{request_type}?q={location}&units={temp_unit}&appid={api_key}"
                    weather_data = requests.get(request_string)
                    weather_arg = tracker.get_slot('weather_arg') #gets the slot value
                    trackers = tracker.current_slot_values()
                    print("Weather Args: ", weather_arg)
                    print("trackers ", trackers)

                    if (weather_data.status_code == requests.codes.ok):#If the request is good
                        weather_data = json.loads(weather_data.text)
                        
                        #Response dictionary build
                        return_dic = {"default":"", "rain":"", "quantity":"", "temp":"", "humidity":"", "clowdy":""}
                        if request_type == "forecast":
                            weather_data = weather_data['list'][time_difference]
                        return_dic['default'] = f"You will be experiencing {weather_data['weather'][0]['description'].lower()}"
                        if weather_arg is not None:
                            for arg in weather_arg:
                                if arg == "rain":
                                    try:
                                        return_dic[arg] = f"up to {weather_data['rain']['1h']} milileters of rain"
                                        if "quantity" not in weather_arg:
                                            return_dic[arg] = "rain"
                                    except:
                                        return_dic[arg] = "no rain"
                                if arg == "temp":
                                    if "metric" in weather_arg:
                                        temp_unit = "Celcius"
                                    elif "imperial" in weather_arg:
                                        temp_unit = "Fahrenheit"
                                    return_dic[arg] = f"temperatures of {weather_data['main']['temp']} {temp_unit}"
                                if arg == "wind":
                                    return_dic[arg] = f"a wind speed of {weather_data['wind']['speed']} miles per hour"
                                if arg == "humidity":
                                    return_dic[arg] = f"a humidity of {weather_data['main']['humidity']} percent" #TODO: humidity verbal descriptors
                                if arg == "clowdy":
                                    return_dic[arg] = f"a clowdiness of {weather_data['clouds']['all']} percent" #TODO: humidity verbal descriptors111
                                if arg == "snowing":
                                    try:
                                        return_dic[arg] = f"up to {weather_data['snow']['1h']} milileters of rain"
                                        if "quantity" not in weather_arg:
                                            return_dic[arg] = "snow"
                                    except:
                                        return_dic[arg] = "no snow"
                                


                        return_string = f"{return_dic['default']} with {return_dic['rain']} {return_dic['quantity']} {return_dic['temp']} {return_dic['humidity']} {return_dic['clowdy']} {time_string} in {location}"
                    
                    dispatcher.utter_message(f"{return_string}")

        except Exception as e:
            print(e)
            dispatcher.utter_message(f"An unexpected error in {self.action_name} has ocurred")

class ActionReminderSet(Action):
    from datetime import datetime, timezone
    from custom_actions.action_reminder_set import CurrentReminders


    def name(self):
        self.action_name = "action_reminder_set"
        return self.action_name

    def run(self, dispatcher, tracker, domain):
        trackers = tracker.current_slot_values()
        print("trackers ", trackers)
        
        reminder = CurrentReminders()
        reminder_string = tracker.get_slot("reminder")
        reminder_date = tracker.get_slot("time")[0][:-6]
        reminder_date = int(datetime.strptime(reminder_date,"%Y-%m-%dT%H:%M:%S.%f").timestamp())
        
        return_string = reminder.set_reminder(reminder_string, reminder_date)
        dispatcher.utter_message(f"{return_string}")


class ActionReminderDelete(Action):
    from custom_actions.action_reminder_set import CurrentReminders

    def name(self):
        self.action_name = "action_reminder_delete"
        return self.action_name

    def run(self, dispatcher, tracker, domain):
        reminder = CurrentReminders()
        reminder_string = tracker.get_slot("reminder")

        return_string = reminder.delete_reminder(reminder_string)
        dispatcher.utter_message(f"{return_string}")

class ActionReminderList(Action):
    from datetime import datetime, timezone
    from custom_actions.action_reminder_set import CurrentReminders

    def name(self):
        self.action_name = "action_reminder_list"
        return self.action_name

    def run(self, dispatcher, tracker, domain):
        reminder = CurrentReminders()
        reminder_date = tracker.get_slot("time")[0][:-6]
        reminder_date = int(datetime.strptime(reminder_date,"%Y-%m-%dT%H:%M:%S.%f").timestamp())

        reminder_thresholds = (reminder_date)
        #TODO: use the from this to this date identifier for ducky
        #TODO: if only one date is input show the reminders for that day
        return_string = reminder.list_reminder(reminder_thresholds)
        dispatcher.utter_message(f"{return_string}")