stories_md = """
## happy path               <!-- name of the story - just for debugging -->
* greet              
  - utter_greet
* mood_great               <!-- user utterance, in format intent[entities] -->
  - utter_happy            <!-- action the bot should execute -->
* mood_affirm
  - utter_happy
* mood_affirm
  - utter_goodbye
  
## strange user
* mood_affirm
  - utter_happy
* mood_affirm
  - utter_unclear

## say goodbye
* goodbye
  - utter_goodbye

## ask weather
* weather_request
  - action_return_weather

## fallback
- utter_unclear
"""