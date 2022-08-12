from StopLightColors import StopLightColor
import requests
import re
import datetime
import json

class WeatherReporter:
    def __init__(self):
        self.name = "Weather"
        self.latest = -1
        self.lastChecked = datetime.datetime(2000,1,1)

    def loadRequired(self):
        delta = datetime.datetime.now() - self.lastChecked
        print('checking delta ' + str(delta))
        return delta.total_seconds() > 5 * 60

    def invalidate(self):
        print(self.name + ' invalidated')
        self.latest = -1
        self.lastChecked = datetime.datetime(2000,1,1)
        
    def loadLatest(self):
        self.latest = -1
        self.lastChecked = datetime.datetime.now()

    def calculateRange(self) -> StopLightColor:
        if self.latest == -1:
            return StopLightColor.ERROR
        elif self.latest < 10:
            return StopLightColor.RED
        elif self.latest < 15:
            return StopLightColor.YELLOW
        else:
            return StopLightColor.GREEN

class NoaaWindReporter(WeatherReporter):
    def __init__(self):
        super().__init__()
        self.name = "NOAA Wind"

    def loadLatest(self):
        try:
            print('retrieving wind from noaa')
            station = 'fbis1'
            r = requests.get("http://www.ndbc.noaa.gov/station_page.php?station=" + station)
            pageContent = r.text
            x = re.search("Continuous Winds((.|\\r|\\n)(?!\\d+\\skts))*\\s*((\\d+)\\s+kts)", pageContent)
            wind = int(x.groups()[3])
            print('wind is ' + str(wind))
            self.latest = wind
            self.lastChecked = datetime.datetime.now()
        except Exception as e:
            print('wind error occurred')
            print(e)
            self.latest -1
            self.lastChecked = datetime.datetime.now()

class AzureWindApiReporter(WeatherReporter):
    def __init__(self):
        super().__init__()
        self.name = "Azure API Wind"

    def loadLatest(self):
        try:
            print('retrieving wind from noaa')
            station = 'fbis1'
            r = requests.get('https://currentwind.azurewebsites.net/WeatherForecast?station=fbis1')
            forecast = json.loads(r.text)
            wind = int(forecast["windSpeed"])
            print('wind is ' + str(wind))
            self.latest = wind
            self.lastChecked = datetime.datetime.now()
        except Exception as e:
            print('wind error occurred')
            print(e)
            self.latest -1
            self.lastChecked = datetime.datetime.now()

class StormGlassSurfReporter(WeatherReporter):
    def __init__(self):
        super().__init__()
        self.name = "StormGlass Surf"

    def loadLatest(self):
        try:
            apikey = '14691b2a-18c2-11ed-a3aa-0242ac130002-14691ba2-18c2-11ed-a3aa-0242ac130002'
            lat = 32.78498
            long = -79.78441
                    
            print('retrieving surf from stormglass')
            response = requests.get(
            'https://api.stormglass.io/v2/weather/point',
            params={
                'lat': lat,
                'lng': long,
                'params': 'waveHeight,wavePeriod',
                'start': '2022-08-10T18:00:00+00:00',
                'end': '2022-08-10T18:59:00+00:00',
                'source': 'sg',
            },
            headers={
                'Authorization': apikey
            }
            )

            # Do something with response data.
            json_data = response.json()
            waveHeight = json_data['hours'][0]['waveHeight']['sg']
            wavePeriod = json_data['hours'][0]['wavePeriod']['sg']
            print('h=' + str(waveHeight) + ', p=' + str(wavePeriod))
            #forecast = json.loads(r.text)
            #       wind = int(forecast["wind"])
            #      print('wind is ' + str(wind))
            self.latest = (waveHeight, wavePeriod)
            print(self.latest)
            self.lastChecked = datetime.datetime.now()
        except Exception as e:
            print('wind error occurred')
            print(e)
            self.latest = (-1, -1)
            self.lastChecked = datetime.datetime.now()

    def calculateRange(self) -> StopLightColor:
        waveHeight, wavePeriod = self.latest
        if waveHeight == -1:
            return StopLightColor.ERROR
        elif waveHeight < 10:
            return StopLightColor.RED
        elif waveHeight < 15:
            return StopLightColor.YELLOW
        else:
            return StopLightColor.GREEN


