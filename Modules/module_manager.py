from Modules import open_weather_map_API as weather
from Modules import reminders

class Module_Manager:
    def __init__(self):
        pass
    def boot_manager(self):
        pass
    def runtime_manager(self, command, sentence):
        #TODO: possibly automate this section so it only loads moduleName.runtime() or something
        mainCommand = list(command.keys())[0]
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