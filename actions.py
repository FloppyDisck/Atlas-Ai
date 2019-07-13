#Custom actions
#conda activate atlasai & python -m rasa_core_sdk.endpoint --actions actions
# in duckling files stack exec duckling-example-exe

#Enviroment vars are setup in ~/.profile, export varName=varValue

#NOTE: tracker.get_slot('') gets a singular slot and current_slot_values() gets all of them; 
# current_state() returns json
from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

from modules import env_var_reader

class ActionWeatherReturn(Action):

    from modules import open_weather_map_API

    def name(self):
        self.actionName = "action_weather_return"
        return self.actionName

    def run(self, dispatcher, tracker, domain):
        #Make module that generates a log file with error
        #Encapsulate all code in a try except with this to prevent program from stopping
        #There has to be default values, like location=place you live
        location = "Puerto Rico"
        request = "weather"
        apiKey = env_var_reader.get_var("OPEN_WEATHER_MAP_API_KEY")
        
        trackers = tracker.current_slot_values()

        dispatchera.utter_message("")


        try:
            
            trackers1 = tracker.get_slot('weather_arg')
            trackers2 = tracker.current_slot_values()
            print("trackers 1", trackers1)
            print("trackers 2", trackers2)
            argList = []
            trackerDic = tracker.current_state()
            for argument in trackerDic['latest_message']['entities']:
                argList.append([argument['text'], argument['value'], argument['entity']])
            print(argList)
            dispatcher.utter_message("Weather text here")
        except Exception as e:
            dispatcher.utter_message(f"{e}")