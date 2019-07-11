#Custom actions
#conda activate atlasai & python -m rasa_core_sdk.endpoint --actions actions
# in duckling files stack exec duckling-example-exe

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

class ActionWeatherReturn(Action):
    def name(self):
        return "action_weather_return"

    def run(self, dispatcher, tracker, domain):
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
            #TODO: tracker.get_latest_entity_values() missing 1 required positional argument: 'entity_type'
        except Exception as e:
            dispatcher.utter_message(f"{e}")