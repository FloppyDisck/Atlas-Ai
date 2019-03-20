from Functions import command_deconstructor
from Functions import open_weather_map_API as weather

sentence = "How is the weather like in 5 days in Puerto Rico??"
print(sentence)
command = command_deconstructor.CommandProcessing()
command.analize_sentence(sentence)
#Voice to text ends here

command.primary_command_identifier() #First passthrough of the command

print(command.secondary_command_identifier())

if (len(command.secondary_command_identifier()) > 0):
        #Continue
        if (list(command.secondary_command_identifier().keys())[0] == "Weather"):
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