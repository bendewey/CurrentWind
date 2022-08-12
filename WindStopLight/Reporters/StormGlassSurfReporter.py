import datetime
import requests
from StopLightColors import StopLightColor
import Reporters.WeatherReporter as WeatherReporter

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
        elif waveHeight < 1 or wavePeriod < 6:
            return StopLightColor.RED
        elif waveHeight < 3 and wavePeriod < 8:
            return StopLightColor.YELLOW
        else:
            return StopLightColor.GREEN


