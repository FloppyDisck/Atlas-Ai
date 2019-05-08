from Processes import command_deconstructor
from Processes import open_weather_map_API as weather
from Processes import reminders

sentence = "Weather ??"
print(sentence)
command = command_deconstructor.CommandProcessing("Processes/DataBases/commandDB")
analizedSentence = command.analize_sentence(sentence)
#Voice to text ends here

print(analizedSentence)

if (len(analizedSentence) > 0):
        #Continue
        mainCommand = list(analizedSentence.keys())[0]
        if (mainCommand == "Weather"):
                import geograpy
                places = geograpy.get_place_context(text=sentence)

                try:

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
                except: 
                        print("Location not found! Reverting to default.")
                        defaultLocation = "Puerto Rico"
                        print(weather.request_Weather(defaultLocation, "weather"))

        if (mainCommand == "Reminder"):
                pass
else:
        #Display error that command was not understood
        pass