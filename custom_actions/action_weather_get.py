class Weather():
    # Default values
    temp_unit = "Celcius"
    request_type = "forecast"
    location = "Puerto Rico"

    def __init__(self, api_key):
        self.api_key = api_key
    def get_weather(self):
        import json, requests
        request_string = f"https://api.openweathermap.org/data/2.5/{self.request_type}?q={self.location}&units={self.temp_unit}&appid={self.api_key}"
        weather_data = requests.get(request_string)
        if (weather_data.status_code == requests.codes.ok):#If the request is good
            weather_data = json.loads(weather_data.text)
            return weather_data
        else:
            return None