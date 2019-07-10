#Custom actions
#conda activate atlasai & python -m rasa_core_sdk.endpoint --actions actions

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

class ActionWeatherReturn(Action):
    def name(self):
        return "action_weather_return"

    def run(self, dispatcher, tracker, domain):
        try:
            #trackers = tracker.get_slot('weather_arg')
            #trackers = tracker.current_slot_values()
            argList = []
            trackerDic = tracker.current_state()
            for argument in trackerDic['latest_message']['entities']:
                argList.append(argument)
            dispatcher.utter_message(trackerDic['latest_message'])
            #TODO: tracker.get_latest_entity_values() missing 1 required positional argument: 'entity_type'
        except Exception as e:
            dispatcher.utter_message(f"{e}")