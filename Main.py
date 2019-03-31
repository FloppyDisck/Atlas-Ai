from Functions import command_deconstructor
from Functions import open_weather_map_API as weather

sentence = "How is the weather like in 5 days in Puerto Rico??"
print(sentence)
command = command_deconstructor.CommandProcessing()
analizedSentence = command.analize_sentence(sentence)
#Voice to text ends here

print(analizedSentence)

if (len(analizedSentence) > 0):
        #Continue
        if (list(analizedSentence.keys())[0] == "Weather"):
                import geograpy3
                places = geograpy3.get_place_context(text=sentence).names
                if len(places) == 0:
                        location = "Puerto Rico"
                else:
                        location = places[0]
                print(weather.request_Weather(location, "weather"))
else:
        #Display error that command was not understood
        pass