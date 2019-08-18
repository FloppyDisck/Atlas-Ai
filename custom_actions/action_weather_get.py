class Weather():
    #Default variables
    temp_unit = "Celcius"
    request_type = "forecast"
    location = "Puerto Rico"
    def __init__(self, api_key):
        self.api_key = api_key
    def get_weather(self):
        import json, requests
        requestSting = f"https://api.openweathermap.org/data/2.5/{self.request_type}?q={self.location}&units={self.temp_unit}&appid={self.api_key}"
        weatherData = requests.get(requestSting)
        if (weatherData.status_code == requests.codes.ok):#If the request is good
            weatherData = json.loads(weatherData.text)
            return weatherData
        else:
            return None