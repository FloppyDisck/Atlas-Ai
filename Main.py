from Functions import command_deconstructor
from Functions import open_weather_map_API as weather

sentence = "How is the weather like in 5 days in Madrid??"
print(sentence)
command = command_deconstructor.CommandProcessing()
analizedSentence = command.analize_sentence(sentence)
#Voice to text ends here

print(analizedSentence)

if (len(analizedSentence) > 0):
        #Continue
        if (list(analizedSentence.keys())[0] == "Weather"):
                from geotext import GeoText

                places = GeoText(sentence).cities
                try:
                        print(weather.request_Weather(location, "weather"))
                except:
                        print("Location not found! Reverting to default.")
                        defaultLocation = "Puerto Rico"
                        print(weather.request_Weather(defaultLocation, "weather"))
else:
        #Display error that command was not understood
        pass