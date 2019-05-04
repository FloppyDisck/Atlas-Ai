from Functions import command_deconstructor
from Functions import open_weather_map_API as weather
from Functions import reminders

sentence = "Weather ??"
print(sentence)
command = command_deconstructor.CommandProcessing()
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
                from datetime import datetime, timezone
                utc_dt = datetime.now(timezone.utc) # UTC time
                dt = utc_dt.astimezone() # local time
                print(utc_dt, dt)
                print(utc_dt.strftime('%s'), dt.strftime('%s'))
else:
        #Display error that command was not understood
        pass