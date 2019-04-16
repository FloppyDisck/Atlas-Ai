from Functions import command_deconstructor
from Functions import open_weather_map_API as weather

sentence = "How is the weather like in 5 days tomorrow in Madrid??"
print(sentence)
command = command_deconstructor.CommandProcessing()
analizedSentence = command.analize_sentence(sentence)
#Voice to text ends here

print(analizedSentence)

if (len(analizedSentence) > 0):
        #Continue
        if (list(analizedSentence.keys())[0] == "Weather"):
                import geograpy
                places = geograpy.get_place_context(text=sentence)

                #TODO: add multivariable searching for 
                # example: "Whats the weather, wind speed and rain volume for the last hour in Madrid"

                if not places.regions:
                        if not places.cities:
                                location = places.countries[0]
                        else:
                                location = places.cities[0]
                else:
                        location = places.regions[0]
                try:
                        print(weather.request_Weather(location, "weather"))
                except:
                        print("Location not found! Reverting to default.")
                        defaultLocation = "Puerto Rico"
                        print(weather.request_Weather(defaultLocation, "weather"))
else:
        #Display error that command was not understood
        pass