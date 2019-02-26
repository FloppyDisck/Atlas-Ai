import speech_recognition as sr

r = sr.Recognizer() #speech recognizer instance

#Start using microphone args - device_index=n
#sr.Microphone.list_microphone_names()
#print the microphones
with sr.Microphone() as source:
    print("Say Something...")
    #Adjust for all the background audio
    r.adjust_for_ambient_noise(source, duration=0.5)
    #Listen to audio and cut
    audio = r.listen(source)

try: #sphinx speech recognizer method
    print("You said: " + r.recognize_sphinx(audio))

except sr.UnknownValueError:
    print("Could no understand audio")

except sr.RequestError as e:
    print("Sphinx error: {0}".format(e))

#RequestError may be thrown if quota limits are met, 
# the server is unavailable, or there is no internet connection.

#TODO: Add a selector to cycle between online recognition 
# and offline pocketSphinx 