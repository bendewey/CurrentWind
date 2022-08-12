import datetime
import requests
import Reporters.WeatherReporter as WeatherReporter

class AzureWindApiReporter(WeatherReporter):
    def __init__(self):
        super().__init__()
        self.name = "Azure API Wind"

    def loadLatest(self):
        try:
            print('retrieving wind from noaa')
            station = 'fbis1'
            r = requests.get('https://currentwind.azurewebsites.net/WeatherForecast?station=fbis1')
            forecast = r.json()
            wind = int(forecast["windSpeed"])
            print('wind is ' + str(wind))
            self.latest = wind
            self.lastChecked = datetime.datetime.now()
        except Exception as e:
            print('wind error occurred')
            print(e)
            self.latest -1
            self.lastChecked = datetime.datetime.now()
