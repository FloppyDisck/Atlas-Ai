import os
os.system("source /etc/environment")
variableName = "OPEN_WEATHER_MAP_API_KEY"
print(f"{variableName} read as {os.environ.get(variableName)}")