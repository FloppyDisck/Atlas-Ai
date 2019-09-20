# in duckling files stack exec duckling-example-exe
# Enviroment vars are setup in ~/.profile, export varName=varValue

#trackers = tracker.current_slot_values()

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
        #Keep enclosed to reduce random errors
        try:
            api_key = get_var("OPEN_WEATHER_MAP_API_KEY")

            weatherReport = Weather(api_key)
            weather_arg = tracker.get_slot('weather_arg')

            # Change temperature units
            if "metric" in weather_arg:
                weatherReport.temp_unit = "Celcius"
            elif "imperial" in weather_arg:
                weatherReport.temp_unit = "Fahrenheit"

            # Change location
            if tracker.get_slot('location') == None:
                weatherReport.location = "Puerto Rico"
            else:
                weatherReport.location = tracker.get_slot('location')

            # Ugly try catch for checking which format added
            try:
                time_command = tracker.get_slot('time')[0][:-6]
                threshold = 0
            except TypeError:
                try:  #Different sentence structures lead to different time slots
                    time_command = tracker.get_slot('time')[0]['to'][:-6]
                    threshold = -1
                except TypeError:
                    time_command = None

            # Check what day were refering too
            time_difference = 0
            time_string = "today"
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
                    print(f"time_command is {time_command}; greater/lower than the allowed parameters")
                    if time_command > 5:
                        time_command = 5
                    elif time_command < 0:
                        time_command = 0
            else:
                print("time_command is None; defaulting to today's weather")
                time_difference = 0

            # Get weather
            weather_data = weatherReport.get_weather()
            weather_data = weather_data['list'][time_difference]
                    
            # Response dictionary build
            return_dic = {"default":"", "connector":"", "rain":"", "quantity":"", "temp":"", "humidity":"", "clowdy":""}
            return_dic['default'] = f"You will be experiencing {weather_data['weather'][0]['description'].lower()}"

            # Build the responce sentence
            if weather_arg is not None:
                return_dic[connector] = "with"
                for arg in weather_arg:
                    if arg == "rain":
                        try:
                            return_dic[arg] = f"up to {weather_data['rain']['1h']} milileters of rain"
                            if "quantity" not in weather_arg:
                                return_dic[arg] = "rain"
                        except:
                            return_dic[arg] = "no rain"
                    if arg == "temp":
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
                    


            return_string = f"{return_dic['default']} {return_dic['connector']} {return_dic['rain']} {return_dic['quantity']} {return_dic['temp']} {return_dic['humidity']} {return_dic['clowdy']} {time_string} over at {weatherReport.location}"
                
            dispatcher.utter_message(f"{return_string}")
        except KeyError:
            dispatcher.utter_message("OPEN_WEATHER_MAP_API_KEY enviroment variable not set!")

        except Exception as e:
            dispatcher.utter_message(f"New Error\n{e}")

class ActionReminderSet(Action):
    from datetime import datetime, timezone
    from custom_actions.action_reminder_set import CurrentReminders


    def name(self):
        self.action_name = "action_reminder_set"
        return self.action_name

    def run(self, dispatcher, tracker, domain):
        from custom_actions.action_reminder_set import CurrentReminders
        
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